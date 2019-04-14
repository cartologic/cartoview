from django.shortcuts import render
from django.shortcuts import get_object_or_404
from cartoview.maps.models import Map
# Create your views here.


def viewer_index(request):
    return render(request, 'viewer/index.html')


def map_view(request, map_id):
    map_obj = get_object_or_404(Map, id=map_id)
    return render(request, 'viewer/index.html', context={'mapId': map_obj.id})


def wagtail_create_map(request):
    return render(request, 'viewer/wagtail_viewer.html')
