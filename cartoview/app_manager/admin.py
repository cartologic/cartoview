from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.contrib import admin
from django.http import HttpResponseServerError
from future import standard_library

from .installer import AppInstaller
from .models import App, AppInstance, AppStore, AppType

standard_library.install_aliases()


def uninstall_selected(modeladmin, request, queryset):
    for app in queryset:
        try:
            app_store = app.store.id if app.store else None
            installer = AppInstaller(
                app.name,
                store_id=app_store,
                user=request.user,
                version=app.version)
            installer.uninstall()
        except Exception as e:
            return HttpResponseServerError(e)


uninstall_selected.short_description = "Uninstall Selected Apps"


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    ordering = ('order',)
    actions = [uninstall_selected]


admin.site.register(AppType)
admin.site.register(AppInstance)
admin.site.register(AppStore)
