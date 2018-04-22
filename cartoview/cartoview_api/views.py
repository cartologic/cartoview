from django.shortcuts import HttpResponse
from geonode.layers.views import layer_detail
import json


def convert_infinty(obj):
    if obj == float('inf') or obj == float('-inf'):
        return None
    else:
        return obj


# TODO: check if function is provided by geonode
def layer_config_json(request, layername):
    layer_details = layer_detail(
        request, layername)
    viewer = layer_details.context_data['viewer']
    layer = layer_details.context_data['resource']
    # TODO: check Projection
    viewer = json.loads(viewer)
    try:
        layer.set_bounds_from_bbox(layer.bbox[0:4], layer.srid)
    except:
        # TODO: remove the following fallback in the new version
        layer.set_bounds_from_bbox(layer.bbox[0:4])
    center = [layer.center_x, layer.center_y]
    zoom = layer.zoom
    viewer['map']['center'] = center
    viewer['map']['zoom'] = zoom
    for l in viewer.get("map").get("layers"):
        if l.get('bbox', None):
            newBBox = []
            for x in l.get('bbox'):
                newBBox.append(convert_infinty(x))
            l.update({"bbox": newBBox})
    return HttpResponse(json.dumps(viewer),
                        content_type="application/json")
