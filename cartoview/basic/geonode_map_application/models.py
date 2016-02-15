from django.db import models
from geonode.maps.models import Map as GeonodeMap
from cartoview.app_manager.models import AppInstance


class BaseMapApp(AppInstance):
    geonode_map = models.ForeignKey(GeonodeMap, related_name="'%(app_label)s_%(class)s'")
    map_config = models.TextField(null=True, blank=True)

    class Meta(AppInstance.Meta):
        abstract = True
