from django.conf.urls import patterns, url
from .views import workspace

urlpatterns = patterns(
    '',
    url('^$', workspace, name="my_workspace"),)
