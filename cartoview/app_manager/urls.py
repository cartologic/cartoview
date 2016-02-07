from django.conf.urls import patterns
from django.views.generic import TemplateView

from api import rest_api
from .rest import AppResource, GeonodeMapResource, GeonodeMapLayerResource
from views import *

rest_api.register(AppResource())
rest_api.register(GeonodeMapResource())
rest_api.register(GeonodeMapLayerResource())

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
        url(r'^(?P<appinstanceid>\d+)/remove$', appinstance_remove, name="appinstance_remove"),
        (r'^rest/', include(rest_api.urls)),
)

apps = get_apps_names()
for name in apps:
    import_app_rest(name)

for name in apps:
    urlpatterns.append(app_url(name))
