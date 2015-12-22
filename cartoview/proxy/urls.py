from django.conf.urls import patterns, url

from views import proxy_view

urlpatterns = patterns(
        '',
        url(r'^(?P<url>.*)$', proxy_view, name='proxy_url'),
)
