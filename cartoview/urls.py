# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import include, url
from django.contrib import admin
from tastypie.api import Api

from cartoview.app_manager.rest import AppResource, AppTypeResource, AppStoreResource, TagResource
from cartoview.views import index, check_version

api = Api(api_name='cartoview-api')
api.register(AppResource())
api.register(AppTypeResource())
api.register(AppStoreResource())
api.register(TagResource())

urlpatterns = [
    url(r'^$', index, name='cartoview_index'),
    url(r'^check-version/$', check_version, name='check_version'),
    url(r'^apps/', include('cartoview.app_manager.urls')),
    url(r'', include(api.urls)),
    url(r'^admin/', admin.site.urls, name="admin")
]
