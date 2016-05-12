from tastypie.resources import ModelResource
from tastypie import fields
from geonode.maps.models import Map as GeonodeMap, MapLayer as GeonodeMapLayer
from geonode.layers.models import Layer, Attribute
from tastypie.constants import ALL_WITH_RELATIONS, ALL

class GeonodeMapLayerResource(ModelResource):
    class Meta:
        queryset = GeonodeMapLayer.objects.distinct()

class GeonodeMapResource(ModelResource):
    map_layers = fields.ToManyField(GeonodeMapLayerResource, 'layer_set', null=True, full=True)
    class Meta:
        queryset = GeonodeMap.objects.distinct().order_by('-date')

class GeonodeLayerResource(ModelResource):
    class Meta:
        queryset = Layer.objects.all()
        excludes = ['csw_anytext', 'metadata_xml']
        filtering = {"typename": ALL}

class GeonodeLayerAttributeResource(ModelResource):
    layer = fields.ForeignKey(GeonodeLayerResource,'layer')
    class Meta:
        queryset = Attribute.objects.all()
        filtering = {"layer": ALL_WITH_RELATIONS}

