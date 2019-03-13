from django.conf.urls import include, re_path
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        re_path(r'^installer/', include('cartoview.app_manager.admin_urls')),
    ]


@hooks.register('register_admin_menu_item')
def register_frank_menu_item():
    return MenuItem(_('Plugins'), reverse('app_installer:index'),
                    classnames='icon icon-folder-inverse', order=300)
