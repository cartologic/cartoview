from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from django.conf.urls import patterns, url
from .views import workspace

urlpatterns = patterns(
    '',
    url('^$', workspace, name="my_workspace"),)
