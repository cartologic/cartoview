
from cartoview.app_manager.models import AppInstance
from geonode.api.resourcebase_api import *
from .resources import  FileUploadResource
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

class AppResource(FileUploadResource):
    class Meta(FileUploadResource.Meta):
        from models import App
        queryset = App.objects.all()
        filtering = {"name": ALL ,"title":ALL}
        can_edit = True




class AppInstanceResource(CommonModelApi):

    app = fields.ToOneField(AppResource, 'app', full=True)
    map = fields.ForeignKey(GeonodeMapResource, 'map', full=True)
    class Meta(CommonMetaApi):
        filtering = CommonMetaApi.filtering

        filtering.update({'app': ALL_WITH_RELATIONS})
        queryset = AppInstance.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'appinstances'

