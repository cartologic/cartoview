from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',
    url('^$', workspace, name="my_workspace"),)
