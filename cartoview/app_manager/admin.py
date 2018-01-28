from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from builtins import *

from django.contrib import admin
from future import standard_library

from .models import App, AppInstance, AppStore, AppType

standard_library.install_aliases()


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    ordering = ('order',)


admin.site.register(AppType)
admin.site.register(AppInstance)
admin.site.register(AppStore)
