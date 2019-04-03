from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from cartoview.connections.utils import get_server_by_value

from .models import Layer

# Register your models here.


@admin.register(Layer)
class LayerAdminModel(GuardedModelAdmin):
    list_display = ("title", "get_server_type",
                    "get_server_url", "projection", "valid")

    def get_server_type(self, obj):
        server = get_server_by_value(obj.server.server_type)
        return server.title
    get_server_type.short_description = "Server Type"
    get_server_type.admin_order_field = "server__server_type"

    def get_server_url(self, obj):
        return obj.server.url
    get_server_url.short_description = "Server URL"
    get_server_url.admin_order_field = "server__url"
