from tastypie.resources import ModelResource
from tastypie import fields
from geonode.maps.models import Map as GeonodeMap, MapLayer as GeonodeMapLayer


class GeonodeMapLayerResource(ModelResource):
    class Meta:
        queryset = GeonodeMapLayer.objects.distinct()

class GeonodeMapResource(ModelResource):
    map_layers = fields.ToManyField(GeonodeMapLayerResource, 'layer_set', null=True, full=True)
    class Meta:
        queryset = GeonodeMap.objects.distinct().order_by('-date')