from django.conf.urls import patterns, url, include
import views
from . import *



urlpatterns = patterns('',
    url(r'^(?P<app_name>[^/]+)/edit/(?P<instance_id>\d+)$', views.edit_app_instance, name=EDIT_INSTANCE_URL_NAME),
    # url(r'^(?P<app_name>[^/]+)/new$', views.new_app_instance, name=NEW_INSTANCE_URL_NAME),
    url(r'^(?P<app_name>[^/]+)/new$', views.NewAppInstanceView.as_view(), name=NEW_INSTANCE_URL_NAME),
)