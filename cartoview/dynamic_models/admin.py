from django.contrib import admin

from .models import Model, ModelField

# Register your models here.


class ModelFieldAdmin(admin.StackedInline):
    list_display = ['name', 'field_type', 'model']
    model = ModelField


@admin.register(Model)
class ModelAdminModel(admin.ModelAdmin):
    inlines = (ModelFieldAdmin,)
    list_display = ['name', 'created']
    actions = ['create_table', 'delete_table']

    def create_table(self, request, queryset):
        for obj in queryset:
            obj.create_table()
        self.message_user(
            request, "Models Were Created")
    create_table.short_description = "Create Model Table"

    def delete_table(self, request, queryset):
        for obj in queryset:
            obj.delete_table()
        self.message_user(
            request, "Models Were Deleted")
    delete_table.short_description = "Delete Model Table"
