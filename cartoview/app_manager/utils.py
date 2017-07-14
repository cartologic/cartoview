# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.conf import settings
from tastypie.serializers import Serializer

from geonode.api.resourcebase_api import LayerResource
from geonode.maps.models import Map


@require_http_methods(["POST", ])
def settings_api(request):
    result = {}
    data = request.POST.getlist('attributes')
    for attr in data:
        if hasattr(settings, attr):
            result[attr] = getattr(settings, attr)
        else:
            return HttpResponse("{} Not Found in settings".format(attr), status=404)
    return JsonResponse(result)



@require_http_methods(["GET", ])
def map_layers(request):
    map_id = request.GET.get('id', None)
    if map_id:
        resource=LayerResource()
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
            bundle = resource.build_bundle(obj=layer)
            dehydrated_obj = resource.full_dehydrate(bundle)
            result['objects'].append(dehydrated_obj)
        data = serializer.serialize(result)
        return HttpResponse(data,content_type='application/json')
    else:
        return HttpResponse("not enough pramters", status=400)
