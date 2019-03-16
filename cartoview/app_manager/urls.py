# -*- coding: utf-8 -*-
from django.urls import include, re_path

from .config import CartoviewApp
from .views import ManageAppsView

app_name = 'app_manager'
urlpatterns = [
    re_path('manage', ManageAppsView.as_view(), name='manage-apps'),
]


def app_url(app_name):
    app = str(app_name)
    return re_path(
        r'^{app_name}/'.format(app_name=app),
        include('%s.urls' % app), name='%s_base_url' % app)


def load_apps_urls():
    app_names = CartoviewApp.objects.get_active_apps().keys()
    for app_name in app_names:
        urlpatterns.append(app_url(app_name))


load_apps_urls()
