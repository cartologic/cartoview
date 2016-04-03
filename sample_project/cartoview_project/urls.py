from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.conf.urls import patterns, url, include
from cartoview.urls import urlpatterns as cartoview_patterns, handler403



urlpatterns = patterns('',

)

urlpatterns += cartoview_patterns