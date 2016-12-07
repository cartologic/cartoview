from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from . import views, APP_NAME

urlpatterns = patterns('',
   url(r'^maps/$', views.list_maps, name='%s.list_maps' % APP_NAME),
   url(r'^maps/(?P<map_id>\d+)/view/$', views.view_map, name='%s.view_map' % APP_NAME),

   url(r'^maps/(?P<map_id>\d+)/embed/$', views.embed_map, name='%s.embed_map' % APP_NAME),
   url(r'^maps/(?P<map_id>\d+)/config.json', views.map_config, name='%s.map_config' % APP_NAME),
   # apps urls
   url(r'^new/$', views.new, name='%s.new' % APP_NAME),
   url(r'^(?P<instance_id>\d+)/edit/$', views.edit, name='%s.edit' % APP_NAME),
   url(r'^(?P<instance_id>\d+)/view/$', views.view_app , name='%s.view' % APP_NAME)
)
