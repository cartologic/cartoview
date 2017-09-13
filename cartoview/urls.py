# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from geonode.urls import urlpatterns
from cartoview.app_manager.rest import AppInstanceResource, AppResource
from cartoview.views import index as cartoview_index, check_version
from cartoview.app_manager.utils import settings_api
from geonode.api.urls import api

api.register(AppInstanceResource())
api.register(AppResource())

urlpatterns = patterns(
    '',
    url(r'^/?$', cartoview_index, name='home'),
    url(r'^check-version/$', check_version, name='check_version'),
    url(r'^settings/api$', settings_api, name='settings-api'),
    url(r'', include(api.urls)),
    (r'^apps/', include('cartoview.app_manager.urls')),
    (r'^workspace/', include('cartoview.workspace.urls')),
    # (r'^engage/', include('cartoview.user_engage.urls')),
    (r'^cartoview_proxy/', include('cartoview.proxy.urls')),) + urlpatterns
