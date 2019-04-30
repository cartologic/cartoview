from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import DataTable


class ModelSchemaAdmin(ModelAdmin):
    model = DataTable
    menu_icon = 'fa-superpowers'  # change as required
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(ModelSchemaAdmin)
