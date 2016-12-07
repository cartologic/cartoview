from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from geonode.maps.models import Map
import json
from guardian.shortcuts import get_objects_for_user
from geonode.maps.views import _resolve_map, _PERMISSION_MSG_VIEW
from cartoview.app_manager.models import AppInstance, App
from django.contrib.auth.decorators import login_required
from cartoview.app_manager.views import _resolve_appinstance
from . import APP_NAME

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
    return render(request, "%s/list_maps.html" % APP_NAME, {'maps':json.dumps(maps)})


def view_map(request, map_id):
    map_obj = _resolve_map(request, map_id, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)
    return render(request, "%s/view_map.html" % APP_NAME, {"map_id": map_id, 'map_obj':map_obj})


def embed_map(request, map_id):
    map_obj = _resolve_map(request, map_id, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)
    return render(request, "%s/view_map.html" % APP_NAME, {"map_id": map_id, 'map_obj': map_obj})


def map_config(request, map_id):
    map_obj = _resolve_map(request, map_id, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)
    config = map_obj.viewer_json(request.user)
    return HttpResponse(json.dumps(config), content_type="application/json")


def save(request, instance_id=None, app_name=APP_NAME):
    res_json = dict(success=False)
    # try:
    map_id = request.POST.get('map', None)
    title = request.POST.get('title', "")
    config = request.POST.get('config', None)
    abstract = request.POST.get('abstract', "")
    if instance_id is None:
        instance_obj = AppInstance()
        instance_obj.app = App.objects.get(name=app_name)
        instance_obj.owner = request.user
    else:
        instance_obj = AppInstance.objects.get(pk=instance_id)
    instance_obj.title = title
    instance_obj.config = config
    instance_obj.abstract = abstract
    instance_obj.map_id = map_id
    instance_obj.save()
    res_json.update(dict(success=True, id=instance_obj.id))
    # except Exception, e:
    #     print e
    #     res_json["error_message"] = str(e)
    return HttpResponse(json.dumps(res_json), content_type="application/json")

@login_required
def new(request, template="%s/edit.html" % APP_NAME, app_name=APP_NAME, context={}):
    if request.method == 'POST':
        return save(request, app_name=app_name)
    return render(request, template, context)

@login_required
def edit(request, instance_id, template="%s/edit.html" % APP_NAME, context={}):
    if request.method == 'POST':
        return save(request, instance_id)
    instance = AppInstance.objects.get(pk=instance_id)
    context.update(instance=instance)
    return render(request, template, context)


def view_app(request, instance_id, template="%s/view_app.html" % APP_NAME, context={}):
    instance = _resolve_appinstance(request, instance_id, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)
    context.update({
        "map_config": instance.map.viewer_json(request.user),
        "instance": instance
    })
    return render(request, template, context)

