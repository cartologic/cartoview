from account.decorators import login_required
from django.shortcuts import render
from cartoview.app_manager.models import App, AppInstance
from geonode.layers.models import Layer
from geonode.maps.models import Map


@login_required
def workspace(request):
    apps = AppInstance.objects.filter(owner=request.user)
    layers = Layer.objects.filter(owner=request.user)
    maps = Map.objects.filter(owner=request.user)
    return render(request, template_name='workspace/workspace.html',context={'my_apps': apps, 'my_layers': layers, 'my_maps': maps})
