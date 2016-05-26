from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from geonode.maps.models import Map
import json
from guardian.shortcuts import get_objects_for_user
from geonode.maps.views import _resolve_map, _PERMISSION_MSG_VIEW


def list_maps(request):
    permitted_ids = get_objects_for_user(request.user,  'base.view_resourcebase').values('id')
    queryset = Map.objects.filter(id__in=permitted_ids)
    maps = []
    for item in queryset:
        maps.append({
            'title': item.title,
            'thumbnail': item.thumbnail_url,
            'id': item.id
        })
    return render(request, "viewer/list_maps.html", {'maps':json.dumps(maps)})


def view_map(request, map_id):
    map_obj = _resolve_map(request, map_id, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)
    return render(request, "viewer/view_map.html", {"map_id": map_id, 'map_obj':map_obj})


def embed_map(request, map_id):
    map_obj = _resolve_map(request, map_id, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)
    return render(request, "viewer/view_map.html", {"map_id": map_id, 'map_obj': map_obj})


def map_config(request, map_id):
    map_obj = _resolve_map(request, map_id, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)
    config = map_obj.viewer_json(request.user)
    return HttpResponse(json.dumps(config), content_type="application/json")