from django.contrib import admin
from .models import Layer
# Register your models here.


@admin.register(Layer)
class LayerAdminModel(admin.ModelAdmin):
    list_display = ('title', 'server_type', 'get_server')

    def get_server(self, obj):
        return obj.server
    get_server.short_description = 'Server'
    get_server.admin_order_field = 'server__title'
