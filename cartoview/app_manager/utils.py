# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import abc
from builtins import *

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from future import standard_library
from future.utils import with_metaclass
from tastypie.serializers import Serializer

from cartoview.app_manager.models import AppInstance
from geonode.api.resourcebase_api import LayerResource
from geonode.maps.models import Map
from django.utils.translation import ugettext as _
from geonode.utils import resolve_object

standard_library.install_aliases()

_PERMISSION_MSG_GENERIC = _("You do not have permissions for this Instance.")


@require_http_methods([
    "GET",
])
def map_layers(request):
    map_id = request.GET.get('id', None)
    layer_type = request.GET.get('layer_type', None)
    if map_id:
        resource = LayerResource()
        serializer = Serializer()
        result = {}
        map_obj = get_object_or_404(Map, id=map_id)
        layers = map_obj.local_layers
        result['meta'] = {}
        result['meta']['limit'] = 1000
        result['meta']['next'] = None
        result['meta']['offset'] = 0
        result['meta']['previous'] = None
        result['meta']['total_count'] = len(layers)
        result['objects'] = []
        for layer in layers:
            bundle = resource.build_bundle(obj=layer, request=request)
            dehydrated_obj = resource.full_dehydrate(bundle)
            # TODO:Test this layer_type filter behavior
            if layer_type:
                qs = layer.attribute_set.filter(
                    attribute_type__icontains=layer_type)
                if qs.count() > 0:
                    dehydrated_obj.data.update(
                        {'layer_type': qs[0].attribute_type})
            else:
                qs = layer.attribute_set.get(attribute_type__contains="gml:")
                dehydrated_obj.data.update(
                    {'layer_type': qs.attribute_type})
            result['objects'].append(dehydrated_obj)
        data = serializer.serialize(result)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponse("not enough pramters", status=400)


def resolve_appinstance(request,
                        appinstanceid,
                        permission='base.change_resourcebase',
                        msg=_PERMISSION_MSG_GENERIC,
                        **kwargs):
    """
    Resolve the document by the provided primary key
    and check the optional permission.
    """
    return resolve_object(
        request,
        AppInstance, {'pk': appinstanceid},
        permission=permission,
        permission_msg=msg,
        **kwargs)


class Thumbnail(with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def create_thumbnail(self):
        """Implement your thumbnail method"""
        pass


class AppsThumbnail(Thumbnail):
    def __init__(self, instance):
        self.instance = instance

    def create_thumbnail(self):
        instance = self.instance
        if not isinstance(instance, AppInstance):
            return
        elif (instance.thumbnail_url is not None or
              instance.thumbnail_url != "") and instance.map is not None:
            parent_app_thumbnail_url = instance.map.get_thumbnail_url()
            instance.thumbnail_url = parent_app_thumbnail_url
            instance.save()
