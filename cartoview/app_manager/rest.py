# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

from cartoview.app_manager.models import App, AppStore, AppType
from cartoview.apps_handler.config import CartoviewApp
from cartoview.log_handler import get_logger
from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from future import standard_library
from taggit.models import Tag
from tastypie import fields, http
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from .installer import AppInstaller, RestartHelper
from .utils import populate_apps

logger = get_logger(__name__)
standard_library.install_aliases()


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


class TagResource(ModelResource):
    class Meta(object):
        queryset = Tag.objects.all()
