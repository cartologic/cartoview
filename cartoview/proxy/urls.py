from django.urls import re_path

from .views import GeoNodeApiProxyView, GeoServerProxyView

urlpatterns = [
    re_path(r'^api/(?P<path>.*)$', GeoNodeApiProxyView.as_view(), name='geonode_api'),
    re_path(r'^geoserver/(?P<path>.*)$', GeoServerProxyView.as_view(), name='geonode_geoserver')
]
