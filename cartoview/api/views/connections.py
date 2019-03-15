# -*- coding: utf-8 -*-
from urllib.parse import unquote

from django.conf import settings
from django.http import HttpResponse
from rest_framework import permissions, status, viewsets
from ..permissions import AuthPermission
from rest_framework.response import Response
from rest_framework.views import APIView

from cartoview.connections import DEFAULT_PROXY_SETTINGS
from cartoview.connections.models import (Server,
                                          SimpleAuthConnection,
                                          TokenAuthConnection)
from cartoview.connections.utils import URL
from cartoview.log_handler import get_logger

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


class ServerProxy(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
            default_headers = proxy_settings.get('default_headers', {})
        accept = request.META.get(
            'HTTP_ACCEPT', default_headers.get('Accept'))
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE',
                                default_headers.get('Accept-Language'))
        headers = {
            'Accept': accept,
            'Accept-Language': lang,
            'Content-Type': request.META.get('CONTENT_TYPE'),
        }
        return headers

    def allowed_to_serve(self, server_url, target_url):
        # NOTE:this method check if target url targeting the server
        return URL.compare_netloc(server_url, target_url)

    def serve(self, request, pk, *args, **kwargs):
        # TODO:handle different types of http methods
        server = Server.objects.get(pk=pk)
        session = server.connection.session
        url = request.GET.get('url', None)
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
                                content_type=req.headers.get('content-type'))
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
