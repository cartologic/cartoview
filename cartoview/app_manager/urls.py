# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib

from django.conf.urls import include, url
from django.views.generic import TemplateView
from future import standard_library

from cartoview.app_manager.rest import (AppInstanceResource, AppResource,
                                        AppStoreResource,
                                        GeonodeMapLayerResource, TagResource)
from cartoview.apps_handler.config import CartoviewApp
from . import views as app_manager_views
from .api import rest_api

standard_library.install_aliases()
rest_api.register(AppResource())
rest_api.register(AppStoreResource())
rest_api.register(AppInstanceResource())
rest_api.register(GeonodeMapLayerResource())
rest_api.register(TagResource())

urlpatterns = [
    url(r'^$', app_manager_views.index, name='app_manager_base_url'),
    url(r'^manage/$', app_manager_views.manage_apps, name='manage_apps'),
    url(r'^install/(?P<store_id>\d+)/(?P<app_name>.*)/(?P<version>.*)/$',
        app_manager_views.install_app,
        name='install_app'),
    url(r'^uninstall/(?P<store_id>\d+)/(?P<app_name>.*)/$',
        app_manager_views.uninstall_app,
        name='cartoview_uninstall_app_url'),
    url(r'^appinstances/$',
        TemplateView.as_view(
            template_name='app_manager/app_instance_list.html'),
        name='appinstance_browse'),
    url(r'^appinstance/(?P<appinstanceid>\d+)/?$',
        app_manager_views.appinstance_detail,
        name='appinstance_detail'),
    url(r'^appinstance/(?P<appinstanceid>\d+)/metadata$',
        app_manager_views.appinstance_metadata,
        name='appinstance_metadata'),
    url(r'^moveup/(?P<app_id>\d+)/$',
        app_manager_views.move_up,
        name='move_up'),
    url(r'^movedown/(?P<app_id>\d+)/$',
        app_manager_views.move_down,
        name='move_down'),
    url(r'^save_app_orders/$',
        app_manager_views.save_app_orders,
        name='save_app_orders'),
    url(r'^(?P<appinstanceid>\d+)/remove$',
        app_manager_views.appinstance_remove,
        name="appinstance_remove"),
    url(r'^rest/', include(rest_api.urls)),
]


def import_app_rest(app_name):
    try:
        # print 'define %s rest api ....' % app_name
        # module_ = importlib.import_module('%s.rest' % app_name)
        importlib.import_module('%s.rest' % app_name)
    except ImportError:
        pass


def app_url(app_name):
    app = str(app_name)
    return url(
        r'^' + app + '/', include('%s.urls' % app), name=app + '_base_url')


def load_apps_urls():
    app_names = CartoviewApp.objects.get_active_apps().keys()
    for app_name in app_names:
        import_app_rest(app_name)
        urlpatterns.append(app_url(app_name))


load_apps_urls()
