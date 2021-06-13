from django.urls import path, re_path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.index),
    path("manage", views.index),
    # pass the current version to the frontend
    path('get_version', views.get_cartoview_version)
]
