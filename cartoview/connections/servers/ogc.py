# -*- coding: utf-8 -*-
import requests
from owslib.crs import Crs
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService

from cartoview.layers.models import Layer
from cartoview.log_handler import get_logger

from ..utils import get_server_by_value
from .base import BaseServer

logger = get_logger(__name__)


class OGCServer(BaseServer):
    @property
    def is_alive(self):
        req = self.session.get(self.url)
        if req.status_code == requests.codes['ok']:
            return True
        else:
            return False

    @property
    def operation_keys(self):
        return [op.name for op in self.service.operations]

    @property
    def getMapURL(self, method='Get'):
        try:
            base_url = next((m.get('url') for m in self.service
                             .getOperationByName('GetMap').methods
                             if m.get('type').lower() == method.lower()))
        except StopIteration:
            base_url = self.server.url
        return base_url

    @property
    def getFeatureURL(self, method='{http://www.opengis.net/wfs}Get'):
        try:
            base_url = next((m.get('url') for m in
                             self.service.getOperationByName('GetFeature')
                             .methods if m.get('type').lower()
                             == method.lower()))
        except StopIteration:
            base_url = self.server.url
        return base_url

    @property
    def service(self):
        ServiceClass = None
        version = None
        server = get_server_by_value(self.server.server_type)
        if server.type == 'wms':
            ServiceClass = WebMapService
            version = '1.1.1'
        elif server.type == 'wfs':
            ServiceClass = WebFeatureService
            version = '1.1.0'
        wms = ServiceClass(self.server.url, version=version,
                           **self.extra_kwargs)
        return wms

    def unique_layers(self):
        layers = self.get_wms_layers()+self.get_wfs_layers()
        seen = set()
        unique = [
            layer for layer in layers if layer.id not in seen
            and not seen.add(layer.id)]
        return unique

    def layer_dict(self, ows_layer):
        extra = ows_layer.__dict__
        extra.pop('parent', None)
        extra_layers = extra.pop('layers', None)
        if extra_layers:
            pass
            # NOTE: Handle nested layers
            # extra_layers = [self.layer_dict(l) for l in extra_layers]
            # extra.update({'layers': extra_layers})
        csr_options = extra.pop('crsOptions', [])
        srids = []
        for srid in csr_options:
            if isinstance(srid, Crs):
                srid = "{}:{}".format(srid.authority, srid.code)
            srids.append(srid)
        extra.update({"crsOptions": srids})
        extra.pop('_children', None)
        title = extra.pop('title')
        abstract = extra.pop('abstract')
        # services = extra.pop('services', [])
        try:
            bbox = ows_layer.boundingBox[:4]
            projection = ows_layer.boundingBox[-1]
        except AttributeError:
            bbox = ows_layer.boundingBoxWGS84
            projection = "EPSG:4326"
        name = extra.pop('id')
        data = {"extra": extra,
                "description": abstract,
                "title": title,
                "name": name,
                "bounding_box": bbox,
                "projection": projection,
                "owner": self.user,
                "server": self.server}
        return data

    def get_wfs_layers(self):
        wfs = self.wfs_service
        items = wfs.items()
        layers = [l[1] for l in items]
        return layers

    def get_service_layers(self):
        service = self.service
        items = service.items()
        layers = [l[1] for l in items]
        return layers

    def get_layers(self):
        return [self.layer_dict(l) for l in self.get_service_layers()]

    def harvest(self):
        created_objs = []
        layers = self.get_layers()
        for layer in layers:
            qs = Layer.objects.filter(
                name=layer['name'], server=layer['server'])
            if qs.count() == 0:
                obj = Layer.objects.create(**layer)
                created_objs.append(obj)
        self.server.operations = self.operations
        self.server.save()
        return created_objs

    @property
    def operations(self):
        data = {}
        ops = self.service.operations
        for op in ops:
            data.update({op.name: {
                'methods': op.methods,
                'formats': op.formatOptions
            }})
        return data
