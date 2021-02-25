# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import include, url, re_path
from django.contrib import admin
from tastypie.api import Api

from cartoview.app_manager.rest import AppResource, AppTypeResource, AppStoreResource, TagResource
from cartoview.views import index, check_version
from cartoview.geonode_allauth_provider.views import ProfileView

api = Api(api_name='cartoview-api')
api.register(AppResource())
api.register(AppTypeResource())
api.register(AppStoreResource())
api.register(TagResource())

urlpatterns = [
    re_path(r'^$', ProfileView.as_view()),
    url(r'^check-version/$', check_version, name='check_version'),
    url(r'^apps/', include('cartoview.app_manager.urls')),
    url(r'', include(api.urls)),
    url(r'^admin/', admin.site.urls, name="admin")
]

# Add allauth urls
urlpatterns += [
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^accounts/profile/', ProfileView.as_view()),
]
