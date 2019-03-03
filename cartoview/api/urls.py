# -*- coding: utf-8 -*-
from django.urls import include, re_path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from .views import AppStoreViewSet, AppTypeViewSet, AppViewSet, UserViewSet

schema_view = get_swagger_view(title='Cartoview API')
app_name = 'api'
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'apps', AppViewSet, 'apps')
router.register(r'apptypes', AppTypeViewSet, 'apptypes')
router.register(r'stores', AppStoreViewSet, 'stores')
urlpatterns = ([
    re_path(r'^swagger$', schema_view),
    re_path(r'^', include(router.urls)),
], 'api')
