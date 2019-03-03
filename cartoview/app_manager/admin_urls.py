from django.conf.urls import re_path

from .views import plugins_view

app_name = 'app_installer'
urlpatterns = [
    re_path(r'^$', plugins_view, name='index'),
]
