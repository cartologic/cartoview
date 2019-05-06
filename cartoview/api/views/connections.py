# -*- coding: utf-8 -*-
from urllib.parse import unquote

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from cartoview.connections import DEFAULT_PROXY_SETTINGS
from cartoview.connections.models import (Server, SimpleAuthConnection,
                                          TokenAuthConnection)
from cartoview.connections.tasks import (delete_invalid_resources,
                                         harvest_task, update_server_resources,
                                         validate_server_resources)
from cartoview.connections.utils import URL, get_handler_class_handler
from cartoview.log_handler import get_logger

from ..permissions import AuthPermission, IsOwnerOrReadOnly
from ..serializers.connections import (ServerSerializer,
                                       SimpleAuthConnectionSerializer,
                                       TokenAuthConnectionSerializer)

logger = get_logger(__name__)


class AuthConnectionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, AuthPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(owner=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SimpleAuthConnectionViewSet(AuthConnectionViewSet):
    queryset = SimpleAuthConnection.objects.all()
    serializer_class = SimpleAuthConnectionSerializer


class TokenAuthConnectionViewSet(AuthConnectionViewSet):
    queryset = TokenAuthConnection.objects.all()
    serializer_class = TokenAuthConnectionSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"],
            permission_classes=[IsOwnerOrReadOnly, ])
    def harvest(self, request, pk=None):
        try:
            server = Server.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            return Response({"details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        harvest_task.delay(server.id)
        return Response({"message":
                         _("Server Resources Will Be Harvest")},
                        status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"],
            permission_classes=[IsOwnerOrReadOnly, ])
    def update_server_resources(self, request, pk=None):
        try:
            server = Server.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            return Response({"details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        update_server_resources.delay(server.id)
        return Response({"message":
                         _("Server Resources Will Be Updated")},
                        status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"],
            permission_classes=[IsOwnerOrReadOnly, ])
    def delete_invalid_resources(self, request, pk=None):
        try:
            server = Server.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            return Response({"details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        delete_invalid_resources.delay(server.id)
        return Response({"message":
                         _("Invalid Server Resources Will Be Deleted")},
                        status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"],
            permission_classes=[IsOwnerOrReadOnly, ])
    def validate_server_resources(self, request, pk=None):
        try:
            server = Server.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            return Response({"details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        validate_server_resources.delay(server.id)
        return Response({"message":
                         _("Server Resources Will Be Validated")},
                        status=status.HTTP_202_ACCEPTED)


class ServerProxy(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_proxy_settings(self):
        key = "proxy"
        connections_settings = getattr(settings, "CARTOVIEW_CONNECTIONS", {})
        proxy_settings = connections_settings.get(
            key, DEFAULT_PROXY_SETTINGS)
        return proxy_settings

    def get_request_data(self, request):
        data = request.data or None
        return data

    def get_default_headers(self, request):
        proxy_settings = self.get_proxy_settings()
        default_headers = {}
        if proxy_settings:
            default_headers = proxy_settings.get("default_headers", {})
        accept = request.META.get(
            "HTTP_ACCEPT", default_headers.get("Accept"))
        lang = request.META.get("HTTP_ACCEPT_LANGUAGE",
                                default_headers.get("Accept-Language"))
        headers = {
            "Accept": accept,
            "Accept-Language": lang,
            "Content-Type": request.META.get("CONTENT_TYPE"),
        }
        return headers

    def allowed_to_serve(self, server_url, target_url):
        # NOTE: this method check if target url targeting the server
        return URL.compare_netloc(server_url, target_url)

    def serve(self, request, pk, *args, **kwargs):
        server = Server.objects.get(pk=pk)
        conn = server.connection
        user = request.user
        allowed = False
        if server.connection:
            if request.method in permissions.SAFE_METHODS:
                allowed = user.has_perm('use_for_read', conn)
            else:
                allowed = user.has_perm('use_for_write', conn)
        if allowed:
            logger.info("ALLOWED To USE SESSION")
            session = server.handler.session
        else:
            logger.info("NOT ALLOWED To USE SESSION")
            session = get_handler_class_handler(
                "NoAuth").requests_retry_session()
        url = request.GET.get("url", None)
        if not url:
            return Response(data={"error": "No URL Provided"},
                            status=status.HTTP_400_BAD_REQUEST)
        url = unquote(url)
        if not self.allowed_to_serve(server.url, url):
            return Response(data={
                "error": "Not Allowed"
            }, status=status.HTTP_401_UNAUTHORIZED)
        logger.info("Recieved.....")
        logger.error(url)
        req = session.request(request.method, url=url,
                              headers=self.get_default_headers(request),
                              data=self.get_request_data(request))

        logger.info("Served.....")
        # TODO: handle error message
        # NOTE: we use content instead of text to handle files
        response = HttpResponse(req.content, status=req.status_code,
                                content_type=req.headers.get("content-type"))
        return response

    def get(self, request, pk, *args, **kwargs):
        return self.serve(request, pk, *args, **kwargs)

    def put(self, request, pk, *args, **kwargs):
        return self.serve(request, pk, *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        return self.serve(request, pk, *args, **kwargs)

    def patch(self, request, pk, *args, **kwargs):
        return self.serve(request, pk, *args, **kwargs)

    def delete(self, request, pk, *args, **kwargs):
        return self.serve(request, pk, *args, **kwargs)
