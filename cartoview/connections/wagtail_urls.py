# -*- coding: utf-8 -*-
from django.urls import re_path
from .wagtail_views import harvest_resources
urlpatterns = [
    re_path(r"^harvest/(?P<server_id>[\d]+)$", harvest_resources, name='harvest_resources'),
]
