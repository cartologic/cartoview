from django.conf.urls import patterns, url, include
from .views import *

urlpatterns = patterns('',
                       url('^$', workspace,name="my_workspace"),)
