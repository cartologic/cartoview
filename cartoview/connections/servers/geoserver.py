# -*- coding: utf-8 -*-
import requests
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
from requests.auth import HTTPBasicAuth
from owslib.crs import Crs
from cartoview.layers.models import Layer
from cartoview.log_handler import get_logger

from ...connections.utils import urljoin
from .base import BaseServer

logger = get_logger(__name__)


class Geoserver(BaseServer):
    @property
    def is_alive(self):
        req = self.session.get(self.status_url)
        logger.info(self.status_url)
        logger.info(req.status_code)
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
        if self.server.resources_type == 'wms':
            ServiceClass = WebMapService
            version = '1.1.1'
        elif self.server.resources_type == 'wfs':
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
        return created_objs

    def status_url(self):
        return urljoin(self.rest, 'about/status')

    @property
    def rest(self):
        return urljoin(self.url, 'rest')
