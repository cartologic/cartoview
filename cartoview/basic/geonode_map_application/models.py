from django.db import models
from geonode.maps.models import Map as GeonodeMap
from cartoview.app_manager.models import AppInstance
import json

class BaseMapApp(AppInstance):
    geonode_map = models.ForeignKey(GeonodeMap, related_name="'%(app_label)s_%(class)s'")
    map_config = models.TextField(null=True, blank=True)

    @property
    def config_obj(self):
        try:
            return json.loads(self.map_config)
        except:
            return {}

    class Meta(AppInstance.Meta):
        abstract = True
