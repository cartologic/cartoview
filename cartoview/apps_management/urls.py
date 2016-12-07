from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^handle_install/(?P<name>[-\w]+)$', handle_install_apps, name='handle_install_apps'),
    url(r'^handle_uninstall/(?P<name>[-\w]+)$', handle_uninstall_apps, name='handle_uninstall_apps'),
    url(r'^confirm_installation/(?P<name>[-\w]+)$', confirm_app_installation, name='confirm_installation')
]
