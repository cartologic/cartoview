# -*- coding: utf-8 -*-
from django.urls import include, re_path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from .views.app_manager import AppStoreViewSet, AppTypeViewSet, AppViewSet
from .views.connections import (ServerProxy, ServerViewSet,
                                SimpleAuthConnectionViewSet,
                                TokenAuthConnectionViewSet)
from .views.layers import LayerViewSet
from .views.users import UserViewSet

schema_view = get_swagger_view(title='Cartoview API')
app_name = 'api'
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'apps', AppViewSet, 'apps')
router.register(r'apptypes', AppTypeViewSet, 'apptypes')
router.register(r'stores', AppStoreViewSet, 'stores')
router.register(r'servers', ServerViewSet, 'servers')
router.register(r'layers', LayerViewSet, 'layers')
router.register(r'simpleauth', SimpleAuthConnectionViewSet, 'simpleauth')
router.register(r'tokenauth', TokenAuthConnectionViewSet, 'tokenauth')
urlpatterns = ([
    re_path(r'^swagger$', schema_view),
    re_path(r'^', include(router.urls)),
    re_path(r'^proxy/(?P<pk>[\d]+)/$',
            ServerProxy.as_view(), name='server_proxy'),
], 'api')
