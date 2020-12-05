# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import re

from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import InvalidPage, Paginator
from django.forms import model_to_dict
from django.urls import reverse
from django.db import transaction
from django.http import Http404
from future import standard_library
from geonode.api.api import ProfileResource
from geonode.api.authorization import GeoNodeAuthorization
from geonode.api.resourcebase_api import (CommonMetaApi, LayerResource,
                                          MapResource, CommonModelApi)
from geonode.maps.models import MapLayer
from geonode.people.models import Profile
from geonode.security.utils import get_visible_resources
from guardian.shortcuts import get_objects_for_user
from taggit.models import Tag
from tastypie import fields, http
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from cartoview.app_manager.models import App, AppInstance, AppStore, AppType
from cartoview.apps_handler.config import CartoviewApp
from cartoview.log_handler import get_logger
from .installer import AppInstaller, RestartHelper
from .utils import populate_apps

logger = get_logger(__name__)
standard_library.install_aliases()


class LayerFilterExtensionResource(LayerResource):
    def build_filters(self, filters=None, **kwargs):
        if filters is None:
            filters = {}
        orm_filters = super(LayerFilterExtensionResource, self).build_filters(
            filters, **kwargs)
        if ('permission' in filters):
            permission = filters['permission']
            orm_filters.update({'permission': permission})
        # NOTE: We change this filter name because it overrides
        # geonode type filter(vector,raster)
        if 'geom_type' in filters:
            layer_type = filters['geom_type']
            orm_filters.update({'geom_type': layer_type})

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        permission = applicable_filters.pop('permission', None)
        # NOTE: We change this filter name from type to geom_type because it
        # overrides geonode type filter(vector,raster)
        layer_geom_type = applicable_filters.pop('geom_type', None)
        filtered = super(LayerFilterExtensionResource, self).apply_filters(
            request, applicable_filters)
        if layer_geom_type:
            filtered = filtered.filter(
                attribute_set__attribute_type__icontains=layer_geom_type)
        if permission is not None:
            try:
                permitted_ids = get_objects_for_user(request.user,
                                                     permission).values('id')
            except BaseException:
                permitted_ids = get_objects_for_user(
                    request.user, permission, klass=filtered).values('id')
            filtered = filtered.filter(id__in=permitted_ids)

        return filtered

    class Meta(LayerResource.Meta):
        resource_name = "layers"
        filtering = dict(LayerResource.Meta.filtering, **dict(typename=ALL))


class GeonodeMapLayerResource(ModelResource):
    class Meta(object):
        queryset = MapLayer.objects.distinct()


class AppStoreResource(ModelResource):
    class Meta:
        always_return_data = True
        authorization = Authorization()
        queryset = AppStore.objects.all()


class AppResource(ModelResource):
    store = fields.ForeignKey(AppStoreResource, 'store', full=False, null=True)
    order = fields.IntegerField()
    active = fields.BooleanField()
    pending = fields.BooleanField()
    categories = fields.ListField()

    default_config = fields.DictField(default={})
    app_instance_count = fields.IntegerField()

    def dehydrate_order(self, bundle):
        carto_app = bundle.obj.config
        if carto_app:
            return carto_app.order
        return 0

    def dehydrate_default_config(self, bundle):
        if bundle.obj.default_config:
            return bundle.obj.default_config
        return {}

    def dehydrate_active(self, bundle):
        active = False
        if bundle.obj.config and not bundle.obj.config.pending:
            active = bundle.obj.config.active
        return active

    def dehydrate_pending(self, bundle):
        app = bundle.obj
        cartoview_app = CartoviewApp.objects.get(app.name)
        return cartoview_app.pending

    def dehydrate_categories(self, bundle):
        return [category.name for category in bundle.obj.category.all()]

    def dehydrate_app_instance_count(self, bundle):
        return bundle.obj.appinstance_set.all().count()

    class Meta():
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
                self._meta.resource_name,
                view,
                trailing_slash(),
            )
        else:
            exp = r"^(?P<resource_name>%s)/%s%s$" % (self._meta.resource_name,
                                                     view, trailing_slash())
        return url(exp, self.wrap_view(view), name=name)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/install%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('install'),
                name="bulk_install"),
            url(r"^(?P<resource_name>%s)/restart-server%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('restart_server'),
                name="restart_server"),
            self._build_url_exp('install'),
            self._build_url_exp('reorder'),
            self._build_url_exp('uninstall', True),
            self._build_url_exp('suspend', True),
            self._build_url_exp('activate', True),
        ]

    def get_err_response(self,
                         request,
                         message,
                         response_class=http.HttpApplicationError):
        data = {
            'error_message': message,
        }
        return self.error_response(
            request, data, response_class=response_class)

    def install(self, request, **kwargs):
        """Install requested apps.
        expected post data structure:
            {"apps":[
                {
                    "app_name":<str>,
                    "store_id":<number>,
                    "version":<str>,
                },
            ],
            "restart":<bool>
            }
        return json contains a list of apps with status and message ex:

        [
            {
                "app_name":<str>,
                "success":<bool>,
                "message":<str>,
            }
        ]
        """
        # from builtins import basestring
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)
        if not (request.user.is_active and request.user.is_staff):
            return self.get_err_response(request,
                                         "this action require staff member",
                                         http.HttpForbidden)
        data = json.loads(request.body)
        apps = data.get("apps", [])
        restart = data.get("restart", False)
        response_data = []
        for app in apps:
            app_name = app.get("app_name")
            store_id = app.get("store_id")
            version = app.get("version")
            app_result = {"app_name": app_name, "success": True, "message": ""}
            # try:
            with transaction.atomic():
                installer = AppInstaller(app_name, store_id, version,
                                         request.user)
                installer.install(restart=False)
            app_result["message"] = "App Installed Successfully"
            response_data.append(app_result)
            # except Exception as ex:
            #     logger.error(ex)
            #     app_result["success"] = False
            #     app_result["message"] = "{0}".format(ex)
            #     response_data.append(app_result)
        if restart:
            RestartHelper.restart_server()
        return self.create_response(
            request, response_data, response_class=http.HttpAccepted)

    def restart_server(self, request, **kwargs):
        # from builtins import basestring
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        if not (request.user.is_active and request.user.is_staff):
            return self.get_err_response(request,
                                         "this action require staff member",
                                         http.HttpForbidden)
        RestartHelper.restart_server()
        return self.create_response(
            request, {"message": "Server Will be Restarted"},
            response_class=http.HttpAccepted)

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
            app.set_active(active)
            populate_apps()
        except ObjectDoesNotExist:
            return http.HttpGone()

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
            app.save()
            cartoview_app = CartoviewApp.objects.get(app.name)
            if cartoview_app:
                cartoview_app.order = app.order
                cartoview_app.commit()
            if i == (len(ids_list) - 1):
                CartoviewApp.save()
        self.log_throttled_access(request)
        return self.create_response(request, {'success': True})


class AppTypeResource(ModelResource):
    apps = fields.ToManyField(
        AppResource, attribute='apps', full=True, null=True)

    class Meta(object):
        queryset = AppType.objects.all()


class AppInstanceResource(CommonModelApi):
    launch_app_url = fields.CharField(null=True, blank=True, use_in='all')
    edit_url = fields.CharField(null=True, blank=True)
    app = fields.ForeignKey(AppResource, 'app', full=True, null=True)
    map = fields.ForeignKey(MapResource, 'related_map', full=True, null=True)
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

    def get_object_list(self, request):
        __inactive_apps = [
            app.id for app in App.objects.all()
            if app.config and not app.config.active
        ]
        __inactive_apps_instances = [
            instance.id for instance in AppInstance.objects.filter(
                app__id__in=__inactive_apps)
        ]
        active_app_instances = super(AppInstanceResource, self) \
            .get_object_list(
            request).exclude(
            id__in=__inactive_apps_instances)

        return active_app_instances

    def format_objects(self, objects):
        # hack needed because dehydrate does not seem to work in CommonModelApi
        formatted_objects = []
        for obj in objects:
            formatted_obj = model_to_dict(obj, fields=self.VALUES)
            formatted_obj['owner__username'] = obj.owner.username
            formatted_obj['owner_name'] = \
                obj.owner.get_full_name() or obj.owner.username
            if obj.app is not None:
                formatted_obj['launch_app_url'] = \
                    reverse("%s.view" % obj.app.name, args=[obj.pk])
                formatted_obj['edit_url'] = \
                    reverse("%s.edit" % obj.app.name, args=[obj.pk])
            formatted_objects.append(formatted_obj)
        return formatted_objects

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

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Get the list of objects that matches the filter
        sqs = self.build_haystack_filters(request.GET)

        if not settings.SKIP_PERMS_FILTER:

            filter_set = get_objects_for_user(request.user,
                                              'base.view_resourcebase')

            filter_set = get_visible_resources(
                filter_set,
                request.user if request else None,
                admin_approval_required=settings.ADMIN_MODERATE_UPLOADS,
                unpublished_not_visible=settings.RESOURCE_PUBLISHING,
                private_groups_not_visibile=settings.GROUP_PRIVATE_RESOURCES)

            filter_set_ids = filter_set.values_list('id')
            # Do the query using the filterset and the query term. Facet the
            # results
            if len(filter_set) > 0:
                sqs = sqs.filter(id__in=filter_set_ids).facet('type').facet(
                    'owner').facet('keywords').facet('regions') \
                    .facet('category')
            else:
                sqs = None
        else:
            sqs = sqs.facet('type').facet('owner').facet('keywords').facet(
                'regions').facet('category')

        if sqs:
            # Build the Facet dict
            facets = {}
            for facet in sqs.facet_counts()['fields']:
                facets[facet] = {}
                for item in sqs.facet_counts()['fields'][facet]:
                    facets[facet][item[0]] = item[1]

            # Paginate the results
            paginator = Paginator(sqs, request.GET.get('limit'))

            try:
                page = paginator.page(int(request.GET.get('offset') or 0)
                                      / int(request.GET.get('limit'), 0) + 1)  # noqa
            except InvalidPage:
                raise Http404("Sorry, no results on that page.")

            if page.has_previous():
                previous_page = page.previous_page_number()
            else:
                previous_page = 1
            if page.has_next():
                next_page = page.next_page_number()
            else:
                next_page = 1
            total_count = sqs.count()
            objects = page.object_list
        else:
            next_page = 0
            previous_page = 0
            total_count = 0
            facets = {}
            objects = []

        object_list = {
            "meta": {
                "limit": settings.CLIENT_RESULTS_LIMIT,
                "next": next_page,
                "offset": int(getattr(request.GET, 'offset', 0)),
                "previous": previous_page,
                "total_count": total_count,
                "facets": facets,
            },
            "objects": map(lambda x: self.get_haystack_api_fields(x), objects),
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    def get_haystack_api_fields(self, haystack_object):
        object_fields = dict(
            (k, v) for k, v in haystack_object.get_stored_fields().items()
            if not re.search('_exact$|_sortable$', k))
        return object_fields

    def prepend_urls(self):
        if settings.HAYSTACK_SEARCH:
            return [
                url(r"^(?P<resource_name>%s)/search%s$" %
                    (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('get_search'),
                    name="api_get_search"),
            ]
        else:
            return []

    def build_haystack_filters(self, parameters):
        from haystack.inputs import Raw
        from haystack.query import SearchQuerySet, SQ  # noqa

        sqs = None

        # Retrieve Query Params

        # Text search
        query = parameters.get('q', None)

        # Types and subtypes to filter (map, layer, vector, etc)
        type_facets = parameters.getlist("type__in", [])

        # If coming from explore page, add type filter from resource_name
        resource_filter = self._meta.resource_name.rstrip("s")
        if resource_filter != "base" and resource_filter not in type_facets:
            type_facets.append(resource_filter)

        # Publication date range (start,end)
        date_end = parameters.get("date__lte", None)
        date_start = parameters.get("date__gte", None)

        # Topic category filter
        category = parameters.getlist("category__identifier__in")

        # Keyword filter
        keywords = parameters.getlist("keywords__slug__in")

        # Region filter
        regions = parameters.getlist("regions__name__in")

        # Owner filters
        owner = parameters.getlist("owner__username__in")

        # app filters
        app = parameters.getlist("app__name__in")

        # Sort order
        sort = parameters.get("order_by", "relevance")

        # Geospatial Elements
        bbox = parameters.get("extent", None)

        # Filter by Type and subtype
        if type_facets is not None:
            types = []

            for type in type_facets:
                if type in ["map", "layer", "document", "user", "appinstance"]:
                    # Type is one of our Major Types (not a sub type)
                    types.append(type)

            if len(types) > 0:
                sqs = (SearchQuerySet() if sqs is None else sqs).narrow(
                    "type:%s" % ','.join(map(str, types)))

        # Filter by Query Params
        # haystack bug? if boosted fields aren't included in the
        # query, then the score won't be affected by the boost
        if query:
            if query.startswith('"') or query.startswith('\''):
                # Match exact phrase
                phrase = query.replace('"', '')
                sqs = (SearchQuerySet() if sqs is None else sqs) \
                    .filter(
                    SQ(title__exact=phrase) | SQ(description__exact=phrase)
                    | SQ(content__exact=phrase))  # noqa
            else:
                words = [
                    w for w in re.split(r'\W', query, flags=re.UNICODE) if w
                ]
                for i, search_word in enumerate(words):
                    if i == 0:
                        sqs = (SearchQuerySet() if sqs is None else sqs) \
                            .filter(
                            SQ(title=Raw(search_word))
                            | SQ(description=Raw(search_word))  # noqa
                            | SQ(content=Raw(search_word))  # noqa
                        )
                    elif search_word in ["AND", "OR"]:
                        pass
                    elif words[i - 1] == "OR":  # previous word OR this word
                        sqs = sqs.filter_or(
                            SQ(title=Raw(search_word))
                            | SQ(description=Raw(search_word))  # noqa
                            | SQ(content=Raw(search_word)))  # noqa
                    else:  # previous word AND this word
                        sqs = sqs.filter(
                            SQ(title=Raw(search_word))
                            | SQ(description=Raw(search_word))  # noqa
                            | SQ(content=Raw(search_word)))  # noqa

        # filter by category
        if category:
            sqs = (SearchQuerySet() if sqs is None else sqs).narrow(
                'category:%s' % ','.join(map(str, category)))

        # filter by keyword: use filter_or with keywords_exact
        # not using exact leads to fuzzy matching and too many results
        # using narrow with exact leads to zero results if multiple keywords
        # selected
        if keywords:
            for keyword in keywords:
                sqs = (SearchQuerySet() if sqs is None else sqs).filter_or(
                    keywords_exact=keyword)

        # filter by regions: use filter_or with regions_exact
        # not using exact leads to fuzzy matching and too many results
        # using narrow with exact leads to zero results if multiple keywords
        # selected
        if regions:
            for region in regions:
                sqs = (SearchQuerySet() if sqs is None else sqs).filter_or(
                    regions_exact__exact=region)

        # filter by owner
        if owner:
            sqs = (SearchQuerySet() if sqs is None else sqs).narrow(
                "owner__username:%s" % ','.join(map(str, owner)))

        # filter by app
        if app:
            sqs = (SearchQuerySet() if sqs is None else sqs).narrow(
                "app__name:%s" % ','.join(map(str, app)))

        # filter by date
        if date_start:
            sqs = (SearchQuerySet() if sqs is None else sqs).filter(
                SQ(date__gte=date_start))

        if date_end:
            sqs = (SearchQuerySet() if sqs is None else sqs).filter(
                SQ(date__lte=date_end))

        # Filter by geographic bounding box
        if bbox:
            left, bottom, right, top = bbox.split(',')
            sqs = (SearchQuerySet() if sqs is None else sqs).exclude(
                SQ(bbox_top__lte=bottom) | SQ(bbox_bottom__gte=top)
                | SQ(bbox_left__gte=right) | SQ(bbox_right__lte=left))  # noqa

        # Apply sort
        if sort.lower() == "-date":
            sqs = (SearchQuerySet() if sqs is None else sqs).order_by("-date")
        elif sort.lower() == "date":
            sqs = (SearchQuerySet() if sqs is None else sqs).order_by("date")
        elif sort.lower() == "title":
            sqs = (SearchQuerySet()
                   if sqs is None else sqs).order_by("title_sortable")
        elif sort.lower() == "-title":
            sqs = (SearchQuerySet()
                   if sqs is None else sqs).order_by("-title_sortable")
        elif sort.lower() == "-popular_count":
            sqs = (SearchQuerySet()
                   if sqs is None else sqs).order_by("-popular_count")
        else:
            sqs = (SearchQuerySet() if sqs is None else sqs).order_by("-date")

        return sqs


class TagResource(ModelResource):
    class Meta(object):
        queryset = Tag.objects.all()
