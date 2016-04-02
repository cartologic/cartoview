from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from geonode.urls import *
from cartoview.app_manager.rest import AppInstanceResource, AppResource

from geonode.api.urls import api
api.register(AppInstanceResource())
api.register(AppResource())

urlpatterns = patterns('',
    url(r'^/?$', TemplateView.as_view(template_name='site_index.html'), name='home'),
    url(r'', include(api.urls)),
    (r'^apps/', include('cartoview.app_manager.urls')),
) + urlpatterns



