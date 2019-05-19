
from urllib.parse import urlparse

import requests

from cartoview.layers.models import Layer

from .base import BaseServer
from cartoview.log_handler import get_logger
logger = get_logger(__name__)


class GeoNode(BaseServer):
    def get_layer_link(self, layer_data, link_type='OGC:WMS'):
        link = None
        layer_links = layer_data.get('links', [])
        for obj in layer_links:
            url_type = obj.get('link_type', None)
            if url_type == link_type:
                link = obj.get('url')
                break
        return link

    def get_layers_model(self, layer_data):
        layer = {}
        # target_link_types = ['OGC:WMS', 'OGC:WFS']
        target_link_types = ['OGC:WMS', ]
        try:
            links = [self.get_layer_link(layer_data, link_type)
                     for link_type in target_link_types]
            link = next(url for url in links if url)
        except StopIteration:
            raise Exception("Can't find layer url")
        layer['url'] = link
        layer['title'] = layer_data.pop('title', None)
        layer['description'] = layer_data.pop('abstract', None)
        layer['name'] = layer_data.pop('alternate', None)
        layer['projection'] = layer_data.pop('srid', None)
        layer['owner'] = self.user
        layer['server'] = self.server
        bbox = [layer_data.pop('bbox_x0', 0),
                layer_data.pop('bbox_y0', 0),
                layer_data.pop('bbox_x1', 0),
                layer_data.pop('bbox_y1', 0)]
        layer['bounding_box'] = [float(coord) for coord in bbox]
        layer['extra'] = layer_data
        return layer

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
                try:
                    layer_data = self.crewl_layer_details(obj, clearedurl)
                    filteredobjects.append(layer_data)
                except BaseException as e:
                    logger.error(str(e))
                    continue
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
