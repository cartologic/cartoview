
from cartoview.app_manager.models import AppInstance, App, AppStore
from geonode.api.resourcebase_api import *
from .resources import  FileUploadResource
from tastypie.resources import ModelResource
from tastypie import fields
from geonode.maps.models import Map as GeonodeMap, MapLayer as GeonodeMapLayer
from geonode.layers.models import Layer, Attribute
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from django.core.urlresolvers import reverse
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from taggit.models import Tag

class GeonodeMapLayerResource(ModelResource):
    class Meta:
        queryset = GeonodeMapLayer.objects.distinct()

class GeonodeMapResource(ModelResource):
    map_layers = fields.ToManyField(GeonodeMapLayerResource, 'layer_set', null=True, full=True)

    class Meta(CommonMetaApi):
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


class AppStoreResource(FileUploadResource):
    class Meta(FileUploadResource.Meta):
        queryset = AppStore.objects.all()


class AppResource(FileUploadResource):
    store = fields.ForeignKey(AppStoreResource, 'store', full=False, null=True)
    class Meta(FileUploadResource.Meta):
        queryset = App.objects.all()
        filtering = {"id": ALL, "name": ALL, "title":ALL , "store": ALL_WITH_RELATIONS}
        can_edit = True


class AppInstanceResource(ModelResource):
    launch_app_url = fields.CharField(null=True, blank=True)
    edit_url = fields.CharField(null=True, blank=True)
    app = fields.ForeignKey(AppResource, 'app', full=False, null=True)
    map = fields.ForeignKey(GeonodeMapResource, 'map', full=True, null=True)
    owner = fields.CharField(null=True, blank=True)

    class Meta(CommonMetaApi):
        filtering = CommonMetaApi.filtering
        always_return_data = True
        filtering.update({'app': ALL_WITH_RELATIONS})
        queryset = AppInstance.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'appinstances'
        allowed_methods = ['get', 'post', 'put']
        excludes = ['csw_anytext', 'metadata_xml']


    def dehydrate_owner(self, bundle):
        return bundle.obj.owner.username

    def dehydrate_launch_app_url(self, bundle):
        if bundle.obj.app is not None:
            return reverse("%s.view" % bundle.obj.app.name, args=[bundle.obj.pk])
        return None

    def dehydrate_edit_url(self, bundle):
        if bundle.obj.owner == bundle.request.user:
            if bundle.obj.app is not None:
                return reverse("%s.edit" % bundle.obj.app.name, args=[bundle.obj.pk])
        return None

    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
        bundle.obj = AppInstance()
        bundle.obj.owner = bundle.request.user
        app_name = bundle.data['appName']
        print app_name
        bundle.obj.app = App.objects.get(name=app_name)
        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)
        return self.save(bundle)



class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()