from django.conf.urls import patterns, url, include
from django.utils import importlib
from django.views.generic import TemplateView
from cartoview.app_manager.rest import AppResource, AppInstanceResource
from views import *
from api import rest_api
rest_api.register(AppResource())

urlpatterns = patterns(
    'cartoview.app_manager',
    url(r'^$', index, name='app_manager_base_url'),
    url(r'^appinstances/$', TemplateView.as_view(template_name='app_manager/app_instance_list.html'),
                           name='appinstance_browse'),
    url(r'^appinstance/(?P<appinstanceid>\d+)/?$', appinstance_detail, name='appinstance_detail'),
    url(r'^appinstance/(?P<appinstanceid>\d+)/metadata$', appinstance_metadata, name='appinstance_metadata'),

    url(r'^install/$', install_app_view, name='install_app'),
    url(r'^ajax_install/$', ajax_install_app, name='ajax_install_app'),
    url(r'^uninstall/(?P<app_name>.*)/$', uninstall_app, name='cartoview_uninstall_app_url'),
    url(r'^moveup/(?P<app_id>\d+)/$', move_up, name='move_up'),
    url(r'^movedown/(?P<app_id>\d+)/$', move_down, name='move_down'),
    url(r'^suspend/(?P<app_id>\d+)/$', suspend_app, name='suspend'),
    url(r'^resume/(?P<app_id>\d+)/$', resume_app, name='resume'),
    url(r'^save_app_orders/$', save_app_orders, name='save_app_orders'),
    (r'^rest/', include(rest_api.urls)),
    #url(r'^appinstance/(?P<appinstanceid>\d+)/?$', 'appinstance_detail', name='appinstance_detail'),
)

apps = get_apps_names()
for name in apps:
    import_app_rest(name)

for name in apps:
    urlpatterns.append(app_url(name))
