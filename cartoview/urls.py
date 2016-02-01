from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from geonode.urls import *

urlpatterns = patterns('',
   url(r'^/?$',
       TemplateView.as_view(template_name='site_index.html'),
       name='home'),
 ) + urlpatterns

if "cartoview.app_manager" in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                    (r'^apps/', include('cartoview.app_manager.urls')),
                    )

from cartoview.app_manager.rest import AppInstanceResource
api.register(AppInstanceResource())
