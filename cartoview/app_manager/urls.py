import importlib
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.conf import settings
from api import rest_api
from cartoview.app_manager.rest import *
from views import *

rest_api.register(AppResource())
rest_api.register(AppStoreResource())
rest_api.register(AppInstanceResource())
rest_api.register(GeonodeMapResource())
rest_api.register(GeonodeMapLayerResource())
rest_api.register(GeonodeLayerResource())
rest_api.register(GeonodeLayerAttributeResource())
rest_api.register(TagResource())

from cartoview.user_engage.rest import *
rest_api.register(ImageResource())
rest_api.register(CommentResource())


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

urlpatterns = patterns('cartoview.app_manager',
    url(r'^$', index, name='app_manager_base_url'),
    url(r'^manage/$', manage_apps, name='manage_apps'),
    url(r'^install/(?P<store_id>\d+)/(?P<app_name>.*)/(?P<version>.*)/$', install_app, name='install_app'),
    url(r'^uninstall/(?P<store_id>\d+)/(?P<app_name>.*)/$', uninstall_app, name='cartoview_uninstall_app_url'),

    url(r'^appinstances/$', TemplateView.as_view(template_name='app_manager/app_instance_list.html'),
        name='appinstance_browse'),
    url(r'^appinstance/(?P<appinstanceid>\d+)/?$', appinstance_detail, name='appinstance_detail'),
    url(r'^appinstance/(?P<appinstanceid>\d+)/metadata$', appinstance_metadata, name='appinstance_metadata'),
    url(r'^moveup/(?P<app_id>\d+)/$', move_up, name='move_up'),
    url(r'^movedown/(?P<app_id>\d+)/$', move_down, name='move_down'),
    url(r'^save_app_orders/$', save_app_orders, name='save_app_orders'),
    url(r'^(?P<appinstanceid>\d+)/remove$', appinstance_remove, name="appinstance_remove"),
    (r'^rest/', include(rest_api.urls)),
)

def import_app_rest(app_name):
    try:
        # print 'define %s rest api ....' % app_name
        module_ = importlib.import_module('%s.rest' % app_name)
    except ImportError:
        pass


def app_url(app_name):
    app = str(app_name)
    return url(r'^' + app + '/', include('%s.urls' % app), name=app + '_base_url')

apps_config = AppsConfig()
for app_config in apps_config:
    import_app_rest(app_config.name)

for app_config in apps_config:
    urlpatterns.append(app_url(app_config.name))
