from functools import lru_cache

import requests

from cartoview.layers.models import Layer

from .base import BaseServer


class ArcGISLayer(BaseServer):
    @lru_cache(maxsize=128)
    def _do_req(self):
        req = self.session.get(self.url, params={"f": "json"})
        return req

    def get_layers(self):
        layers = []
        req = self._do_req()
        if req.status_code == requests.codes['ok']:
            layers.append(self.layer_dict(req.json()))
        return layers

    def get_projection(self, data):
        projection_number = None
        try:
            srs = data["extent"]["spatialReference"]
            if "latestWkid" in srs:
                projection_number = srs["latestWkid"]
            elif srs["wkid"] == 102100:
                projection_number = 3857
            projection_number = srs["wkid"]
        except BaseException:
            projection_number = 4326
        return "EPSG:{}".format(projection_number)

    def get_extent(self, data):
        extent = data["extent"]
        return list(extent.values())[:4]

    def layer_dict(self, layer_json):
        extra = layer_json
        title = name = extra.pop('name')
        abstract = extra.pop('description')
        data = {"extra": extra,
                "description": abstract,
                "title": title,
                "name": name,
                "bounding_box": self.get_extent(extra),
                "projection": self.get_projection(extra),
                "owner": self.user,
                "server": self.server}
        return data

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
    def is_alive(self):
        req = self._do_req()
        if req.status_code == requests.codes['ok']:
            return True
        else:
            return False

    @property
    def operations(self):
        return list()
