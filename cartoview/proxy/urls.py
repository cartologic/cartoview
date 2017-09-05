from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import *
from django.conf.urls import patterns, url

from .views import proxy_view

urlpatterns = patterns(
    '',
    url(r'^(?P<url_name>[^/]+)/(?P<sub_url>.*)$',
        proxy_view,
        name='cartoview_proxy'),)
