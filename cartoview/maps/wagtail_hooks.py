from django.conf.urls import re_path
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from .views import wagtail_create_map


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        re_path(r'^viewer/', wagtail_create_map, name="wagtail_create_map"),
    ]


@hooks.register('register_admin_menu_item')
def register_frank_menu_item():
    return MenuItem(_('Create New Map'), reverse('wagtail_create_map'),
                    classnames='icon icon-plus', order=400)
