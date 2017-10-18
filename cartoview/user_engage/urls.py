from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from builtins import *

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from future import standard_library

standard_library.install_aliases()

urlpatterns = patterns(
    '',
    url(r'^$',
        TemplateView.as_view(template_name='test.html'),
        name='test_user_engage'),)
