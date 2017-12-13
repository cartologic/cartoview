# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from geonode.urls import urlpatterns
from cartoview.app_manager.rest import (AppInstanceResource, AppResource,
                                        AppTypeResource)
from cartoview.views import index as cartoview_index, check_version
from geonode.api.urls import api

api.register(AppInstanceResource())
api.register(AppResource())
api.register(AppTypeResource())

urlpatterns = patterns(
    '',
    url(r'^/?$', cartoview_index, name='home'),
    url(r'^check-version/$', check_version, name='check_version'),
    url(r'', include(api.urls)),
    (r'^apps/', include('cartoview.app_manager.urls')),) + urlpatterns
