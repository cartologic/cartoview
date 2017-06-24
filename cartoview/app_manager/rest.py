import json
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
from tastypie.http import HttpGone

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
    order = fields.IntegerField()
    active = fields.BooleanField()

    def dehydrate_order(self, bundle):
        return bundle.obj.config.order

    def dehydrate_active(self, bundle):
        return bundle.obj.config.active

    class Meta(FileUploadResource.Meta):
        queryset = App.objects.all().order_by('order')
        filtering = {"id": ALL, "name": ALL, "title":ALL , "store": ALL_WITH_RELATIONS}
        can_edit = True

    def _build_url_exp(self, view, single=False):
        name = view + "_app"
        if single:
            exp = r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/%s%s$" % (self._meta.resource_name, view, trailing_slash(),)
        else:
            exp = r"^(?P<resource_name>%s)/%s%s$" % (self._meta.resource_name, view, trailing_slash())
        return url(exp, self.wrap_view(view), name=name)

    def prepend_urls(self):
        return [
            self._build_url_exp('install'),
            self._build_url_exp('reorder'),
            self._build_url_exp('uninstall', True),
            self._build_url_exp('suspend', True),
            self._build_url_exp('activate', True),
        ]

    def install(self, request, **kwargs):
        pass

    def uninstall(self, request, **kwargs):
        pass

    def set_active(self, active, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)
        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
            app = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
            app.config.active = active
            app.apps_config.save()
        except ObjectDoesNotExist:
            return HttpGone()

        self.log_throttled_access(request)
        return self.create_response(request, {'success': True})

    def suspend(self, request, **kwargs):
        return self.set_active(False, request, **kwargs)

    def activate(self, request, **kwargs):
        return self.set_active(True, request, **kwargs)

    def reorder(self, request, **kwargs):
        ids_list = request.POST.get("apps", None)
        if ids_list is not None:
            ids_list = ids_list.split(",")
        else:
            ids_list = json.loads(request.body)["apps"]
        for i in range(0, len(ids_list)):
            app = App.objects.get(id=ids_list[i])
            app.order = i + 1
            app.config.order = app.order
            app.save()
            if i == (len(ids_list) - 1):
                app.apps_config.save()
        self.log_throttled_access(request)
        return self.create_response(request, {'success': True})

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