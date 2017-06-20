from django.contrib import admin
from models import App, AppTag, AppInstance, AppStore,Logo
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    ordering = ('order',)
# admin.site.register(App)
admin.site.register(AppTag)
admin.site.register(AppInstance)
admin.site.register(AppStore)
admin.site.register(Logo)
