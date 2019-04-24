
from urllib.parse import urlparse

import requests

from cartoview.layers.models import Layer

from .base import BaseServer


class GeoNode(BaseServer):

    def get_layers_model(self, layer):
        filtered = {}
        filtered['title'] = layer.pop('title', None)
        filtered['description'] = layer.pop('abstract', None)
        filtered['name'] = layer.pop('name', None)
        filtered['projection'] = layer.pop('srid', None)
        filtered['owner'] = self.user
        filtered['server'] = self.server
        filtered['bounding_box'] = [layer.pop('bbox_x0', None),
                                    layer.pop('bbox_y0', None),
                                    layer.pop('bbox_x1', None),
                                    layer.pop('bbox_y1', None)]
        filtered['extra'] = layer
        return filtered

    def crewl_layer_details(self, obj, clearedurl):
        response = self.session.get(clearedurl + '/' + str(obj['id']))
        return self.get_layers_model(response.json())

    def get_layers(self, url, filteredobjects):
        parsedurl = urlparse(self.url)
        clearedurl = parsedurl.scheme + '://' + parsedurl.netloc + parsedurl.path
        response = self.session.get(url)
        if response.status_code == requests.codes['ok']:
            layers = response.json()
            objects = layers.get('objects', [])
            for obj in objects:
                filteredobjects.append(
                    self.crewl_layer_details(obj, clearedurl))
            meta = layers.get('meta', None)
            if meta.get('next', None):
                url = parsedurl.scheme + '://' + \
                    parsedurl.netloc + meta['next']
                self.get_layers(url, filteredobjects)
        return filteredobjects

    def harvest(self):
        created_objs = []
        layers = self.get_layers(self.url, [])
        for layer in layers:
            qs = Layer.objects.filter(
                name=layer['name'], server=layer['server'])
            if qs.count() == 0:
                obj = Layer.objects.create(**layer)
                created_objs.append(obj)
        return created_objs

    @property
    def is_alive(self):
        return None

    @property
    def operations(self):
        return None
