from django.conf.urls import patterns, url, include
from .views import *

urlpatterns = patterns('',
                       url('^$', workspace, name="my_workspace"),
                       url('^activities$', my_activities, name="my_activities"), )
