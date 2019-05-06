from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from .models import Server, SimpleAuthConnection, TokenAuthConnection
from .wagtail_urls import urlpatterns as wagtail_urls_patterns


class ServerButtonHelper(ButtonHelper):

    def harvest_button(self, obj):
        btn_classes = ['button-small', 'icon']
        text = _('Harvest Resources')
        return {
            'url': reverse('harvest_resources', kwargs={"server_id": obj.id}),
            'label': text,
            'classname': self.finalise_classname(btn_classes),
            'title': text,
        }

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        """
        This function is used to gather all available buttons.
        We append our custom button to the btns list.
        """
        btns = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude)
        if 'view' not in (exclude or []):
            btns.append(
                self.harvest_button(obj)
            )
        return btns


@hooks.register('register_admin_urls')
def register_admin_urls():
    return wagtail_urls_patterns


class ServerModelAdmin(ModelAdmin):
    model = Server
    menu_label = 'GIS Servers'
    menu_icon = 'plus-inverse'
    menu_order = 201
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'url', 'server_type',
                    'owner')
    list_filter = ('title', 'url', 'server_type', 'owner__username')
    button_helper_class = ServerButtonHelper


class SimpleAuthConnectionAdmin(ModelAdmin):
    model = SimpleAuthConnection
    menu_label = 'Simple Auth'
    menu_order = 203
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('username', 'server')
    list_filter = ('username',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)


class TokenAuthConnectionAdmin(ModelAdmin):
    model = TokenAuthConnection
    menu_label = 'Token Auth'
    menu_order = 204
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('token', 'prefix')
    list_filter = ('prefix',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)


modeladmin_register(ServerModelAdmin)
modeladmin_register(SimpleAuthConnectionAdmin)
modeladmin_register(TokenAuthConnectionAdmin)
