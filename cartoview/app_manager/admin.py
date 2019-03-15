# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import App, AppStore, AppType, AppInstance
from guardian.admin import GuardedModelAdmin
# Register your models here.


@admin.register(App)
class AppModelAdmin(GuardedModelAdmin):
    pass


@admin.register(AppStore)
class AppStoreModelAdmin(admin.ModelAdmin):
    pass


@admin.register(AppType)
class AppTypeModelAdmin(admin.ModelAdmin):
    pass


@admin.register(AppInstance)
class AppInstanceModelAdmin(admin.ModelAdmin):
    pass
