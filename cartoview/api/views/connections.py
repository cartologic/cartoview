# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from cartoview.connections.models import Server
from cartoview.log_handler import get_logger
from cartoview.connections.utils import URL
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE
from ..serializers.connections import ServerSerializer
from cartoview.connections import DEFAULT_PROXY_SETTINGS
logger = get_logger(__name__)


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
        url = request.GET.get('url')
        if not self.allowed_to_serve(server.url, url):
            return Response(data={
                "error": "Not Allowed"
            }, status=HTTP_406_NOT_ACCEPTABLE)
        data = self.get_request_data(request)
        logger.info("Recieved.....")
        logger.info(data)
        req = session.request(request.method, url=url,
                              headers=self.get_default_headers(request),
                              data=self.get_request_data(request))

        logger.info("Served.....")
        # TODO: handle error message
        response = HttpResponse(req.text, status=req.status_code,
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
