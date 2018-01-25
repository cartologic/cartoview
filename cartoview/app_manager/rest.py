# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
from builtins import *
from cartoview.app_manager.models import App, AppInstance, AppStore, AppType
from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from future import standard_library
from geonode.api.api import ProfileResource
from geonode.api.authorization import GeoNodeAuthorization
from geonode.api.resourcebase_api import CommonMetaApi
from geonode.layers.models import Attribute, Layer
from geonode.maps.models import Map as GeonodeMap
from geonode.maps.models import MapLayer as GeonodeMapLayer
from geonode.people.models import Profile
from guardian.shortcuts import get_objects_for_user
from taggit.models import Tag
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.http import HttpGone
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from .resources import FileUploadResource
from geonode.api.resourcebase_api import LayerResource
standard_library.install_aliases()


class LayerFilterExtensionResource(LayerResource):
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(LayerFilterExtensionResource, self).build_filters(filters)
        if('permission' in filters):
            permission = filters['permission']
            orm_filters.update({'permission': permission})
        if 'type' in filters:
            layer_type = filters['type']
            orm_filters.update({'type': layer_type})

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        permission = applicable_filters.pop('permission', None)
        layer_type = applicable_filters.pop('type', None)
        filtered = super(LayerFilterExtensionResource, self).apply_filters(
            request, applicable_filters)
        if layer_type:
            filtered = filtered.filter(
                attribute_set__in=Attribute.objects.filter(
                    attribute_type__icontains=layer_type))
        if permission is not None:
            filtered = get_objects_for_user(request.user, permission,
                                            filtered)
        return filtered

    class Meta(LayerResource.Meta):
        resource_name = "layers"
        filering = LayerResource.Meta.filtering
        filering.update({
            'typename': ALL
        })


class GeonodeMapLayerResource(ModelResource):
    class Meta(object):
        queryset = GeonodeMapLayer.objects.distinct()


# TODO: remove this Resource


class GeonodeMapResource(ModelResource):
    map_layers = fields.ToManyField(
        GeonodeMapLayerResource, 'layer_set', null=True, full=True)

    class Meta(CommonMetaApi):
        queryset = GeonodeMap.objects.distinct().order_by('-date')


class GeonodeLayerResource(ModelResource):

    class Meta(object):
        queryset = Layer.objects.all()
        excludes = ['csw_anytext', 'metadata_xml']
        filtering = {"typename": ALL}


class GeonodeLayerAttributeResource(ModelResource):
    layer = fields.ForeignKey(GeonodeLayerResource, 'layer')

    class Meta(object):
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
    categories = fields.ListField()
    app_instance_count = fields.IntegerField()

    def dehydrate_order(self, bundle):
        return bundle.obj.config.order

    def dehydrate_active(self, bundle):
        return bundle.obj.config.active

    def dehydrate_categories(self, bundle):
        return [category.name for category in bundle.obj.category.all()]

    def dehydrate_app_instance_count(self, bundle):
        return bundle.obj.appinstance_set.all().count()

    class Meta(FileUploadResource.Meta):
        queryset = App.objects.all().order_by('order')
        filtering = {
            "id": ALL,
            "name": ALL,
            "title": ALL,
            "store": ALL_WITH_RELATIONS,
            "single_instance": ALL
        }
        can_edit = True

    def _build_url_exp(self, view, single=False):
        name = view + "_app"
        if single:
            exp = r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/%s%s$" % (
                self._meta.resource_name, view, trailing_slash(),)
        else:
            exp = r"^(?P<resource_name>%s)/%s%s$" % (self._meta.resource_name,
                                                     view, trailing_slash())
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
            bundle = self.build_bundle(
                data={'pk': kwargs['pk']}, request=request)
            app = self.cached_obj_get(
                bundle=bundle, **self.remove_api_resource_names(kwargs))
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


class AppTypeResource(ModelResource):
    apps = fields.ToManyField(
        AppResource, attribute='apps', full=True, null=True)

    class Meta(object):
        queryset = AppType.objects.all()


class AppInstanceResource(ModelResource):
    launch_app_url = fields.CharField(null=True, blank=True)
    edit_url = fields.CharField(null=True, blank=True)
    app = fields.ForeignKey(AppResource, 'app', full=True, null=True)
    map = fields.ForeignKey(GeonodeMapResource, 'map', full=True, null=True)
    owner = fields.ForeignKey(
        ProfileResource, 'owner', full=True, null=True, blank=True)
    keywords = fields.ListField(null=True, blank=True)

    class Meta(CommonMetaApi):
        filtering = CommonMetaApi.filtering
        always_return_data = True
        filtering.update({'app': ALL_WITH_RELATIONS, 'featured': ALL})
        queryset = AppInstance.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'appinstances'
        allowed_methods = ['get', 'post', 'put']
        excludes = ['csw_anytext', 'metadata_xml']
        authorization = GeoNodeAuthorization()

    def dehydrate_owner(self, bundle):
        return bundle.obj.owner.username

    def dehydrate_config(self, bundle):
        if bundle.obj.config:
            return json.loads(bundle.obj.config)
        else:
            return json.dumps({})

    def dehydrate_launch_app_url(self, bundle):
        if bundle.obj.app is not None:
            return reverse(
                "%s.view" % bundle.obj.app.name, args=[bundle.obj.pk])
        return None

    def dehydrate_edit_url(self, bundle):
        if bundle.obj.owner == bundle.request.user:
            if bundle.obj.app is not None:
                return reverse(
                    "%s.edit" % bundle.obj.app.name, args=[bundle.obj.pk])
        return None

    def hydrate_owner(self, bundle):
        owner, created = Profile.objects.get_or_create(
            username=bundle.data['owner'])
        bundle.data['owner'] = owner
        return bundle

    def dehydrate_keywords(self, bundle):
        return bundle.obj.keyword_list()

    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
        bundle.obj = AppInstance()
        bundle.obj.owner = bundle.request.user
        app_name = bundle.data['appName']
        bundle.obj.app = App.objects.get(name=app_name)
        for key, value in list(kwargs.items()):
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)
        return self.save(bundle)


class TagResource(ModelResource):

    class Meta(object):
        queryset = Tag.objects.all()
