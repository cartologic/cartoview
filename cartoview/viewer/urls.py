from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
   url(r'^maps/(?P<map_id>\d+)/view/$', views.view_map, name='viewer.view_map'),
   url(r'^maps/(?P<map_id>\d+)/embed/$', views.embed_map, name='viewer.embed_map'),
   url(r'^maps/(?P<map_id>\d+)/config.json', views.map_config, name='viewer.map_config'),
)
