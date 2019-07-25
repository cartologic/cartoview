from urllib.parse import urlparse

import requests
from cartoview.layers.models import Layer
from cartoview.log_handler import get_logger
from cartoview.maps.models import Map

from .base import BaseServer

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
        parsedurl = urlparse(clearedurl)
        url = parsedurl.scheme + '://' + parsedurl.netloc + obj.get('resource_uri')
        response = self.session.get(url)
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

    def get_maps(self, url, filteredobjects):
        response = requests.get(self.url + "/api/maps")
        if response.status_code == requests.codes['ok']:
            maps = response.json()
            objects = maps.get('objects', [])
            for obj in objects:
                try:
                    if not Map.objects.filter(geonode_id=obj['id']).exists():
                        temp_map = Map(title=obj['title'], geonode_id=obj['id'])
                        temp_map.save()
                    filteredobjects.append(temp_map)
                except BaseException as e:
                    logger.error(str(e))
                    continue
        return filteredobjects

    def harvest(self):
        created_objs = []
        maps = self.get_maps(self.url, [])
        for map_obj in maps:
            # qs = Map.objects.filter(
            #     title=map_obj['title'])
            # if qs.count() == 0:
            #     obj = Map.objects.create(**map_obj)
            #     created_objs.append(obj)
            obj = Map.objects.create(**map_obj)
            created_objs.append(obj)
        return created_objs

    @property
    def is_alive(self):
        return None

    @property
    def operations(self):
        return None
