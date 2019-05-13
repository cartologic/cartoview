from django.conf.urls import include, re_path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import (ModelAdmin, ModelAdminGroup,
                                                modeladmin_register)
from wagtail.core import hooks

from .models import AppStore


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        re_path(r'^installer/', include('cartoview.app_manager.admin_urls')),
    ]


class AppStoreModelAdmin(ModelAdmin):
    model = AppStore
    menu_label = 'App Store'
    menu_icon = 'fa-cloud'
    menu_order = 201
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'url', 'server_type', 'is_default')
    list_filter = ('name', 'url', 'server_type', 'is_default')


class ServerGroup(ModelAdminGroup):
    menu_label = 'Plugins'
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (AppStoreModelAdmin,)

    def get_submenu_items(self):
        menu_items = super(ServerGroup, self).get_submenu_items()
        menu_items.append(MenuItem(_('Plugins'), reverse_lazy('app_installer:index'),
                                   classnames='icon icon-fa-th-large', order=4))
        return menu_items


modeladmin_register(ServerGroup)
