# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib import admin
from django.urls import include, path
from tastypie.api import Api

from cartoview.app_manager.rest import AppResource, AppTypeResource, AppStoreResource, TagResource
from cartoview.geonode_allauth_provider.views import ProfileView
from cartoview.views import check_version

api = Api(api_name='api')
api.register(AppResource())
api.register(AppTypeResource())
api.register(AppStoreResource())
api.register(TagResource())

urlpatterns = [
    # /
    path('', ProfileView.as_view()),
    # /api/
    path('', include(api.urls)),
    # /check-version/
    path('check-version/', check_version, name='check_version'),
    # /apps
    path('apps/', include('cartoview.app_manager.urls')),
    # /admin/
    path('admin/', admin.site.urls, name="admin")
]

# Add allauth urls
urlpatterns += [
    path('^accounts/', include('allauth.urls')),
    path('^accounts/profile/', ProfileView.as_view()),
]
