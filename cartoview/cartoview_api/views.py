# -*- coding: utf-8 -*-
import requests
from django.shortcuts import HttpResponse
from geonode.geoserver.helpers import ogc_server_settings
from geonode.layers.views import (_PERMISSION_MSG_MODIFY, _resolve_layer,
                                  layer_detail)
from requests.auth import HTTPBasicAuth

from cartoview.log_handler import get_logger

try:
    import simplejson as json
except BaseException:
    import json
logger = get_logger(__name__)


def convert_infinty(obj):
    if obj == float('inf') or obj == float('-inf'):
        return None
    else:
        return obj


def get_geoserver_credintials():
    gs_user = ogc_server_settings.credentials[0]
    gs_password = ogc_server_settings.credentials[1]
    gs_url = ogc_server_settings.LOCATION
    return gs_user, gs_password, gs_url


def layer_config_json(request, layername):
    layer_details = layer_detail(
        request, layername)
    viewer = layer_details.context_data['viewer']
    layer = layer_details.context_data['resource']
    viewer = json.loads(viewer)
    try:
        layer.set_bounds_from_bbox(layer.bbox[0:4], layer.srid)
    except BaseException:
        layer.set_bounds_from_bbox(layer.bbox[0:4])
    center = [layer.center_x, layer.center_y]
    zoom = layer.zoom
    viewer['map']['center'] = center
    viewer['map']['zoom'] = zoom
    for mapLayer in viewer.get("map").get("layers"):
        if mapLayer.get('bbox', None):
            newBBox = []
            for x in mapLayer.get('bbox'):
                newBBox.append(convert_infinty(x))
            mapLayer.update({"bbox": newBBox})
    return HttpResponse(json.dumps(viewer),
                        content_type="application/json")


def get_featureType(workspace, store, lyr_name):
    gs_user, gs_password, gs_url = get_geoserver_credintials()
    target_url = "{}rest/workspaces/{}/datastores/{}/featuretypes/{}" \
        .format(
        gs_url, workspace, store, lyr_name)
    req = requests.get(target_url,
                       headers={'Accept': 'application/json'},
                       auth=HTTPBasicAuth(gs_user, gs_password))
    return json.loads(req.content)


def update_extent(request, typename):
    lyr = _resolve_layer(
        request,
        typename,
        'base.change_resourcebase',
        _PERMISSION_MSG_MODIFY)
    store = lyr.store
    workspace = lyr.workspace
    lyr_name = lyr.name
    feature_type = get_featureType(workspace, store, lyr_name)
    gs_user, gs_password, gs_url = get_geoserver_credintials()
    target_url = "{}rest/workspaces/{}/datastores/{}/featuretypes/{}" \
        .format(
        gs_url, workspace, store, lyr_name)
    req = requests.put(target_url + "?recalculate=nativebbox,latlonbbox",
                       json=feature_type,
                       headers={'Accept': 'application/json'},
                       auth=HTTPBasicAuth(gs_user, gs_password))
    if req.status_code == 200:
        new_feature_type = get_featureType(workspace, store, lyr_name)
        native_bbox = new_feature_type["featureType"]["nativeBoundingBox"]
        bbox = [native_bbox["minx"], native_bbox["maxx"],
                native_bbox["miny"], native_bbox["maxy"]]
        # srid = native_bbox["crs"]
        try:
            lyr.set_bounds_from_bbox(bbox, lyr.srid)
        except BaseException:
            lyr.set_bounds_from_bbox(bbox)
        lyr.save()
    return HttpResponse(json.dumps({"msg": "Success"}),
                        content_type="application/json")
