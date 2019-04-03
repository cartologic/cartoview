# -*- coding: utf-8 -*-
from urllib.parse import unquote

from django.conf import settings
from django.http import HttpResponse
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from cartoview.connections import DEFAULT_PROXY_SETTINGS
from cartoview.connections.models import Server
from cartoview.connections.utils import URL, get_handler_class_handler
from cartoview.log_handler import get_logger

from ..permissions import IsOwnerOrReadOnly
from ..serializers.connections import ServerSerializer

logger = get_logger(__name__)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


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
        # NOTE:this method check if target url targeting the server
        return URL.compare_netloc(server_url, target_url)

    def serve(self, request, pk, *args, **kwargs):
        # TODO:handle different types of http methods
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
