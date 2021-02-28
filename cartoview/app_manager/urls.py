# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib

from django.urls import include, path, re_path
from future import standard_library

from cartoview.app_manager.config import CartoviewApp
from . import views as app_manager_views

standard_library.install_aliases()

urlpatterns = [
    # /apps/
    path('', app_manager_views.index, name='app_manager_base_url'),
    # /apps/manage/
    path('manage/', app_manager_views.manage_apps, name='manage_apps'),

    path('install/<int:store_id>/<app_name>/<version>/',
         app_manager_views.install_app,
         name='install_app'),
    path('uninstall/<int:store_id>/<app_name>/',
         app_manager_views.uninstall_app,
         name='cartoview_uninstall_app_url'),
    path('moveup/<int:app_id>/',
         app_manager_views.move_up,
         name='move_up'),
    path('movedown/<int:app_id>/',
         app_manager_views.move_down,
         name='move_down'),
    path('save_app_orders/',
         app_manager_views.save_app_orders,
         name='save_app_orders'),
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
    return re_path(
        r'^' + app + '/', include('%s.urls' % app), name=app + '_base_url')


def load_apps_urls():
    app_names = CartoviewApp.objects.get_active_apps().keys()
    for app_name in app_names:
        import_app_rest(app_name)
        urlpatterns.append(app_url(app_name))


load_apps_urls()
