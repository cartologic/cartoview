from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from django.contrib import admin
from future import standard_library
from .installer import AppInstaller
from .models import App, AppInstance, AppStore, AppType
standard_library.install_aliases()


def uninstall_selected(modeladmin, request, queryset):
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied
    for app in queryset:
        try:
            app_store = app.store.id if app.store else None
            installer = AppInstaller(
                app.name, store_id=app_store, user=request.user)
            installer.uninstall()
        except Exception as e:
            return HttpResponseServerError(e.message)


uninstall_selected.short_description = "Uninstall Selected Apps"


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    ordering = ('order', )
    actions = [uninstall_selected]


admin.site.register(AppType)
admin.site.register(AppInstance)
admin.site.register(AppStore)
