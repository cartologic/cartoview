from django.contrib import admin
from models import App, AppTag, AppInstance, AppStore

admin.site.register(App)
admin.site.register(AppTag)
admin.site.register(AppInstance)
admin.site.register(AppStore)
