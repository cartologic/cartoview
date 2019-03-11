# -*- coding: utf-8 -*-
import requests
from owslib.wms import WebMapService
from requests.auth import HTTPBasicAuth

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

    def layer_dict(self, ows_layer):
        extra = ows_layer.__dict__
        extra.pop('parent', None)
        extra.pop('_children', None)
        title = extra.pop('title')
        abstract = extra.pop('abstract')
        name = extra.pop('name')
        data = {"extra": extra,
                "description": abstract,
                "title": title,
                "name": name,
                "bounding_box": ows_layer.boundingBox[:4],
                "projection": ows_layer.boundingBox[-1],
                "server": self.server
                }
        return data

    def get_ows_layers(self):
        wms = self.wms_service
        items = wms.items()
        layers = [l[1] for l in items]
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
    def status_url(self):
        return urljoin(self.rest, 'about/status')

    @property
    def rest(self):
        return urljoin(self.url, 'rest')
