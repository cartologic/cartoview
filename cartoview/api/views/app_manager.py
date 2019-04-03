# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from pkg_resources import parse_version
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cartoview.app_manager.exceptions import AppAlreadyInstalledException
from cartoview.app_manager.installer import AppInstaller
from cartoview.app_manager.models import App, AppInstance, AppStore, AppType
from cartoview.log_handler import get_logger

from ..permissions import AppPermission
from ..serializers.app_manager import (AppInstanceSerializer, AppSerializer,
                                       AppStoreSerializer, AppTypeSerializer)
from ..filters import AppFilter, AppInstanceFilter
logger = get_logger(__name__)


class AppStoreViewSet(viewsets.ModelViewSet):
    queryset = AppStore.objects.all()
    serializer_class = AppStoreSerializer
    permission_classes = (permissions.IsAdminUser,)


class AppTypeViewSet(viewsets.ModelViewSet):
    queryset = AppType.objects.all()
    serializer_class = AppTypeSerializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(installed_by=self.request.user)


class AppInstanceViewSet(viewsets.ModelViewSet):
    queryset = AppInstance.objects.all().prefetch_related("app_map")
    serializer_class = AppInstanceSerializer
    filterset_class = AppInstanceFilter

    def perform_create(self, serializer):
        serializer.save(installed_by=self.request.user)


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = (AppPermission,)
    filterset_class = AppFilter

    def perform_create(self, serializer):
        serializer.save(installed_by=self.request.user)

    @action(detail=False, methods=["post"],
            permission_classes=[AppPermission])
    def install(self, request):
        data = request.data
        app_name = data.get("app_name", None)
        store_id = data.get("store_id", None)
        version = data.get("app_version", None)
        if not app_name or not store_id or not version:
            return Response({"details": "invalid data"}, status=400)
        qs = App.objects.filter(name=app_name)
        if qs.count() > 0:
            permitted = request.user.has_perm("install_app", qs.first())
            if not permitted:
                return Response({"details":
                                 "You don't have permission to install <> app".
                                 format(app_name)}, status=403)
            if parse_version(version) <= parse_version(qs.first().version):
                return Response({"details": "app already installed"},
                                status=400)

        try:
            installer = AppInstaller(
                app_name, store_id, version, user=request.user)
            installer.install()
        except BaseException as e:
            if isinstance(e, AppAlreadyInstalledException):
                logger.warn(e)
            return Response({"details": str(e)}, status=500)
        serializer = AppSerializer(App.objects.get(name=app_name))
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["delete"],
            permission_classes=[AppPermission])
    def uninstall(self, request, pk=None):
        try:
            app = App.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response("App Not Found to uninstall", status=404)
        try:
            installer = AppInstaller(
                app.name, app.store.id, app.version, user=request.user)
            installer.uninstall()
        except BaseException as e:
            return Response({"details": str(e)}, status=500)
        serializer = AppSerializer(app)
        return Response(serializer.data, status=200)
