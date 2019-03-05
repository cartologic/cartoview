# -*- coding: utf-8 -*-
from rest_framework import viewsets

from cartoview.connections.models import Server

from ..serializers.connections import ServerSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
