from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import DataTable


class ModelSchemaAdmin(ModelAdmin):
    model = DataTable
    menu_icon = 'fa-superpowers'
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name', 'description', 'additional_info')


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(ModelSchemaAdmin)
