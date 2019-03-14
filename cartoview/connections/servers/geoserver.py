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
    def wms_service(self):
        username = None
        password = None
        if isinstance(self.session.auth, HTTPBasicAuth):
            username = self.session.auth.username
            password = self.session.auth.password
        # TODO handle other auth type
        wms = WebMapService(self.wms_url, version='1.1.1', username=username,
                            password=password)
        return wms

    @property
    def wfs_service(self):
        username = None
        password = None
        if isinstance(self.session.auth, HTTPBasicAuth):
            username = self.session.auth.username
            password = self.session.auth.password
        # TODO handle other auth type
        wfs = WebFeatureService(url=self.wfs_url, version='1.1.0',
                                username=username,
                                password=password)
        return wfs

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
        services = extra.pop('services', [])
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
                "server": self.server,
                "services": services}
        return data

    def get_wfs_layers(self):
        wfs = self.wfs_service
        items = wfs.items()
        layers = [l[1] for l in items]
        return layers

    def get_wms_layers(self):
        wms = self.wms_service
        items = wms.items()
        layers = [l[1] for l in items]
        return layers

    def get_ows_layers(self):
        wms_layers = self.get_wms_layers()
        wfs_layers = self.get_wfs_layers()
        layers = self.unique_layers()
        for layer in layers:
            layer.services = []
            if any(l.id == layer.id for l in wfs_layers):
                layer.services.append('WFS')
            if any(l.id == layer.id for l in wms_layers):
                layer.services.append('WMS')
        return layers

    def get_layers_data(self):
        return [self.layer_dict(l) for l in self.get_ows_layers()]

    def get_layers(self):
        return self.get_layers_data()

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

    @property
    def wms_url(self):
        return urljoin(self.url, 'wms')

    @property
    def wfs_url(self):
        return urljoin(self.url, 'wfs')

    @property
    def status_url(self):
        return urljoin(self.rest, 'about/status')

    @property
    def rest(self):
        return urljoin(self.url, 'rest')
