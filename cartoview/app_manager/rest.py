from tastypie.constants import ALL
from cartoview.app_manager.models import AppInstance
from geonode.api.resourcebase_api import *
from .resources import BaseModelResource , FileUploadResource
from geonode.maps.models import Map as GeonodeMap, MapLayer as GeonodeMapLayer
from tastypie.resources import ModelResource
from tastypie import fields

class AppResource(FileUploadResource):
    class Meta(FileUploadResource.Meta):
        from models import App
        queryset = App.objects.all()
        filtering = {"name": ALL ,"title":ALL}
        can_edit = True




class AppInstanceResource(CommonModelApi):

    app = fields.ToOneField(AppResource, 'app', full=True)
    class Meta(CommonMetaApi):
        filtering = CommonMetaApi.filtering

        filtering.update({'app': ALL_WITH_RELATIONS})
        queryset = AppInstance.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'appinstances'



class GeonodeMapLayerResource(ModelResource):
    class Meta:
        queryset = GeonodeMapLayer.objects.distinct()


class GeonodeMapResource(ModelResource):
    map_layers = fields.ToManyField(GeonodeMapLayerResource, 'layer_set', null=True, full=True)
    class Meta:
        queryset = GeonodeMap.objects.distinct().order_by('-date')