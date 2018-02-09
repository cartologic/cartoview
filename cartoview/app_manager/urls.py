# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib
from builtins import *

from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from future import standard_library

from cartoview.app_manager.rest import (AppInstanceResource, AppResource,
                                        AppStoreResource,
                                        GeonodeLayerAttributeResource,
                                        GeonodeLayerResource,
                                        GeonodeMapLayerResource,
                                        GeonodeMapResource, TagResource)
from cartoview.app_manager.utils import map_layers

from . import views as app_manager_views
from .api import rest_api
from .config import AppsConfig

standard_library.install_aliases()
rest_api.register(AppResource())
rest_api.register(AppStoreResource())
rest_api.register(AppInstanceResource())
rest_api.register(GeonodeMapResource())
rest_api.register(GeonodeMapLayerResource())
rest_api.register(GeonodeLayerResource())
rest_api.register(GeonodeLayerAttributeResource())
rest_api.register(TagResource())

# from django.conf import settings
#
# for app_name in settings.CARTOVIEW_APPS:
#     # print app_name
#     try:
#         # ensure that the folder is python module
#         app_module = importlib.import_module(app_name + ".rest")
#     except:
#         # TODO: log the error
#         pass

urlpatterns = patterns(
    'cartoview.app_manager',
    url(r'^$', app_manager_views.index, name='app_manager_base_url'),
    url(r'^manage/$', app_manager_views.manage_apps, name='manage_apps'),
    url(r'^install/(?P<store_id>\d+)/(?P<app_name>.*)/(?P<version>.*)/$',
        app_manager_views.install_app,
        name='install_app'),
    url(r'^uninstall/(?P<store_id>\d+)/(?P<app_name>.*)/$',
        app_manager_views.uninstall_app,
        name='cartoview_uninstall_app_url'),
    url(r'^appinstances/$', TemplateView.as_view(
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
    url(r'^save_app_orders/$', app_manager_views.save_app_orders,
        name='save_app_orders'),
    url(r'^(?P<appinstanceid>\d+)/remove$',
        app_manager_views.appinstance_remove,
        name="appinstance_remove"),
    (r'^rest/', include(rest_api.urls)),
    url(r'^maplayers/api$', map_layers, name="cartoview_map_layers"), )


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
        r'^' + app + '/',
        include('%s.urls' % app),
        name=app + '_base_url')


apps_config = AppsConfig()
for app_config in apps_config:
    import_app_rest(app_config.name)

for app_config in apps_config:
    urlpatterns.append(app_url(app_config.name))
