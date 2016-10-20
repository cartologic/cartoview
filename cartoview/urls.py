from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from geonode.urls import urlpatterns
from cartoview.app_manager.rest import AppInstanceResource, AppResource
from cartoview.views import index as cartoview_index

from geonode.api.urls import api
api.register(AppInstanceResource())
api.register(AppResource())

urlpatterns = patterns('',
    url(r'^/?$', cartoview_index, name='home'),
    url(r'^geonode/', TemplateView.as_view(template_name='site_index.html'), name='geonode_home'),
    url(r'', include(api.urls)),
    (r'^apps/', include('cartoview.app_manager.urls')),
    (r'^engage/', include('cartoview.user_engage.urls')),
    # (r'^pages/', include('cartoview.pages.urls')),
    # (r'^viewer/', include('cartoview.viewer.urls')),
    (r'^cartoview_proxy/', include('cartoview.proxy.urls')),
) + urlpatterns



