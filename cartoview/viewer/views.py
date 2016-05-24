from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from geonode.maps.models import Map
import json


def view_map(request, map_id):
    map_obj = Map.objects.get(pk=map_id)
    return render(request, "viewer/index.html", {"map_id": map_id})


def embed_map(request, map_id):
    map_obj = Map.objects.get(pk=map_id)
    return render(request, "viewer/index.html", {})


def map_config(request, map_id):
    map_obj = Map.objects.get(pk=map_id)
    config = map_obj.viewer_json(request.user)
    return HttpResponse(json.dumps(config), content_type="application/json")