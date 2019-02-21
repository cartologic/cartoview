# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from cartoview.app_manager.models import App, AppStore, AppType
from .permissions import AppPermission
from .serializers import (AppSerializer, AppStoreSerializer, AppTypeSerializer,
                          UserSerializer)
from rest_framework import permissions


class AppStoreViewSet(viewsets.ModelViewSet):
    queryset = AppStore.objects.all()
    serializer_class = AppStoreSerializer
    permissions_classes = (permissions.IsAdminUser,)


class AppTypeViewSet(viewsets.ModelViewSet):
    queryset = AppType.objects.all()
    serializer_class = AppTypeSerializer
    permissions_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(installed_by=self.request.user)


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permissions_classes = (AppPermission,)

    def perform_create(self, serializer):
        serializer.save(installed_by=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
