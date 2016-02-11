from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from geonode.urls import *
from cartoview.app_manager.rest import AppInstanceResource

api.register(AppInstanceResource())

urlpatterns = patterns('',
                       url(r'^/?$', TemplateView.as_view(template_name='site_index.html'), name='home'),
                       # add api.urls(it is already added by geonode) after add cartoview resources to update urls.
                       # TODO: find better solution.
                       url(r'', include(api.urls)),
                       ) + urlpatterns

urlpatterns += patterns('',
                        (r'^apps/', include('cartoview.app_manager.urls')),
                        )
