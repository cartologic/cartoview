
from cartoview.app_manager.models import AppInstance
from geonode.api.resourcebase_api import *
from .resources import  FileUploadResource
from tastypie.resources import ModelResource
from tastypie import fields
from geonode.maps.models import Map as GeonodeMap, MapLayer as GeonodeMapLayer
from geonode.layers.models import Layer, Attribute
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from django.core.urlresolvers import reverse

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
        queryset = Attribute.objects.all().order_by('display_order')
        filtering = {
            "layer": ALL_WITH_RELATIONS,
            "id": ALL,
            "attribute": ALL_WITH_RELATIONS
        }


class AppResource(FileUploadResource):
    class Meta(FileUploadResource.Meta):
        from models import App
        queryset = App.objects.all()
        filtering = {"name": ALL ,"title":ALL}
        can_edit = True




class AppInstanceResource(ModelResource):
    launch_app_url = fields.CharField(null=True, blank=True)
    app = fields.ToOneField(AppResource, 'app', full=True, null=True)
    map = fields.ForeignKey(GeonodeMapResource, 'map', full=True, null=True)


    class Meta(CommonMetaApi):
        filtering = CommonMetaApi.filtering

        filtering.update({'app': ALL_WITH_RELATIONS})
        queryset = AppInstance.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'appinstances'

    def dehydrate_launch_app_url(self, bundle):
        if bundle.obj.app is not None:
            return reverse("%s.view" % bundle.obj.app.name, args=[bundle.obj.pk])
        return None
