# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import include, url
from geonode.urls import urlpatterns as geonode_urls

from cartoview.views import check_version

urlpatterns = [
    url(r'^check-version/$', check_version, name='check_version'),
    url(r'^apps/', include('cartoview.app_manager.urls')),
]
urlpatterns += geonode_urls
