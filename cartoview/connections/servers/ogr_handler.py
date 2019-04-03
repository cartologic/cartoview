import os
import re
import time
from contextlib import contextmanager
from functools import lru_cache
from uuid import uuid4

from django.conf import settings

from cartoview.app_manager.os_utils import create_direcotry
from cartoview.layers.models import Layer
from cartoview.log_handler import get_logger

from .base import BaseServer

try:
    import ogr
except ImportError:
    from osgeo import ogr
logger = get_logger(__name__)


class ORGHandler(BaseServer):
    def get_projection(self, layer):
        srs = layer.GetSpatialRef()
        data = {
            "proj4": srs.ExportToProj4(),
            "projcs": srs.GetAttrValue('projcs'),
            "geocs": srs.GetAttrValue('geogcs'),
            "code": "EPSG:%s" % srs.GetAuthorityCode(None)
        }
        return data

    @contextmanager
    def open_source(self, source_path):
        source = ogr.Open(source_path)
        yield source
        source.FlushCache()
        source = None

    def layer_dict(self, layer):
        name = title = layer.GetName()
        abstract = layer.GetDescription()
        bbox = layer.GetExtent()
        proj_dict = self.get_projection(layer)
        projection = proj_dict.get('code', "EPSG:4326")
        fields = [{"name": field.GetName(), "type": field.GetTypeName()}
                  for field in layer.schema]
        extra = {"schema": fields}
        data = {"extra": extra,
                "description": abstract,
                "title": title,
                "name": name,
                "bounding_box": bbox,
                "projection": projection,
                "owner": self.user,
                "server": self.server}
        return data

    @lru_cache(maxsize=256)
    def get_layers(self):
        layers = []
        if self.is_alive():
            with self.open_source(self.url) as datasource:
                count = datasource.GetLayerCount()
                layers = [self.layer_dict(
                    datasource.GetLayerByIndex(i)) for i in range(count)]
        return layers

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
        return data

    def is_alive(self):
        url = self.url
        resp = self.session.get(url)
        return resp.ok


class GeoJSON(ORGHandler):
    pass


class KML(ORGHandler):
    def get_kml_file(self, url):
        file_path = None
        with self.session.get(url, stream=True) as resp:
            resp.raise_for_status()
            header = resp.headers.get('content-disposition', None)
            kml_name = re.findall(
                "filename=(.+)", header)[0] if header else "download.kml"
            dir_path = self.get_new_dir()
            file_path = os.path.join(dir_path, kml_name)
            with open(file_path, 'wb') as kml_file:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        kml_file.write(chunk)
            return file_path

    def get_new_dir(self):
        rand_str = uuid4().__str__().replace('-', '')[:8]
        timestr = time.strftime("%Y/%m/%d/%H/%M/%S")
        target = os.path.join(settings.MEDIA_ROOT,
                              "%s" % self.server.id, timestr, rand_str)
        create_direcotry(target)
        return target

    @contextmanager
    def open_source(self, url):
        driver = ogr.GetDriverByName('KML')
        source = driver.Open(self.get_kml_file(url))
        # source = ogr.Open(source_path)
        yield source
        source.FlushCache()
        source = None
