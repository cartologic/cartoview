from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import *
from django.contrib import admin
from .models import App, AppTag, AppInstance, AppStore, Logo


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    ordering = ('order',)


# admin.site.register(App)
admin.site.register(AppTag)
admin.site.register(AppInstance)
admin.site.register(AppStore)
admin.site.register(Logo)
