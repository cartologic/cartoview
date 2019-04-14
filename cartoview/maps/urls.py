# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import viewer_index, map_view
app_name = 'maps'
urlpatterns = [
    re_path(r"^viewer$", viewer_index, name='viewer_index'),
    re_path(r"^viewer/(?P<map_id>[\d]+)$", map_view, name='map_view'),
]
