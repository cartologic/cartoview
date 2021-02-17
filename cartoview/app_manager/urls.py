# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib

from django.conf.urls import include, url
from future import standard_library

from . import views as app_manager_views

standard_library.install_aliases()

urlpatterns = [
    url(r'^$', app_manager_views.index, name='app_manager_base_url'),
    url(r'^manage/$', app_manager_views.manage_apps, name='manage_apps'),
    url(r'^install/(?P<store_id>\d+)/(?P<app_name>.*)/(?P<version>.*)/$',
        app_manager_views.install_app,
        name='install_app'),
    url(r'^uninstall/(?P<store_id>\d+)/(?P<app_name>.*)/$',
        app_manager_views.uninstall_app,
        name='cartoview_uninstall_app_url'),
    url(r'^moveup/(?P<app_id>\d+)/$',
        app_manager_views.move_up,
        name='move_up'),
    url(r'^movedown/(?P<app_id>\d+)/$',
        app_manager_views.move_down,
        name='move_down'),
    url(r'^save_app_orders/$',
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
    return url(
        r'^' + app + '/', include('%s.urls' % app), name=app + '_base_url')


def load_apps_urls():
    app_names = CartoviewApp.objects.get_active_apps().keys()
    for app_name in app_names:
        import_app_rest(app_name)
        urlpatterns.append(app_url(app_name))


load_apps_urls()
