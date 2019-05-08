from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import DataTable


class DataTablesAdmin(ModelAdmin):
    model = DataTable
    menu_icon = 'fa-superpowers'
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name', 'description', 'additional_info')


modeladmin_register(DataTablesAdmin)
