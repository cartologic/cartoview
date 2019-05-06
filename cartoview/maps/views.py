from django.shortcuts import get_object_or_404, render

from cartoview.maps.models import Map

# Create your views here.


def viewer_index(request):
    return render(request, 'viewer/index.html')


def map_view(request, map_id):
    map_obj = get_object_or_404(Map, id=map_id)
    return render(request, 'viewer/index.html', context={'mapId': map_obj.id})


def wagtail_create_map(request):
    return render(request, 'viewer/wagtail_viewer.html')


def wagtail_edit_map(request, map_id):
    map_obj = get_object_or_404(Map, id=map_id)
    print(map_obj.id)
    return render(request, 'viewer/wagail_edit_map.html',
                  context={'mapId': map_obj.id})
