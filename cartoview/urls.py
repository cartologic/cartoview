# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import include, url
from geonode.api.urls import api
from geonode.urls import urlpatterns as geonode_urls

from cartoview.app_manager.rest import (AppInstanceResource, AppResource,
                                        AppTypeResource,
                                        LayerFilterExtensionResource)
from cartoview.cartoview_api.views import layer_config_json, update_extent
from cartoview.views import check_version
from .cartoview_api.rest import (AllResourcesResource, AttributeResource,
                                 ExtendedResourceBaseResource,
                                 MapLayerResource)

api.register(AppInstanceResource())
api.register(AppResource())
api.register(AppTypeResource())
api.register(LayerFilterExtensionResource())
api.register(AllResourcesResource())
api.register(AttributeResource())
api.register(MapLayerResource())
api.register(ExtendedResourceBaseResource())
urlpatterns = [
    url(r'^layer/(?P<layername>[^/]*)/json/?$', layer_config_json, name='layer_json'),
    url(r'^update/extent/(?P<typename>[^/]*)$', update_extent, name='cartoview.update_extent'),
    url(r'^check-version/$', check_version, name='check_version'),
    url(r'', include(api.urls)),
    url(r'^cv_apps/', include('cartoview.app_manager.urls')),
]
urlpatterns += geonode_urls
