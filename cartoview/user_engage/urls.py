from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
        url(r'^$', TemplateView.as_view(template_name='test.html'), name='test_user_engage'),
)
