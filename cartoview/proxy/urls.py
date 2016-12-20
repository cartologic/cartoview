from django.conf.urls import patterns, url

from views import proxy_view

urlpatterns = patterns(
        '',
        url(r'^http://localhost:4041/(?P<url_name>[^/]+)/(?P<sub_url>.*)$', proxy_view, name='fake_cartoview_proxy'),
        url(r'^(?P<url_name>[^/]+)/(?P<sub_url>.*)$', proxy_view, name='cartoview_proxy'),
)

