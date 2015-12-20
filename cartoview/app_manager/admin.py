from django.contrib import admin

from models import *

# Register your models here.
admin.site.register(App)
admin.site.register(AppTag)
admin.site.register(AppInstance)