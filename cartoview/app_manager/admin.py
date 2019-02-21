# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import App, AppStore, AppType
# Register your models here.


@admin.register(App)
class AppModelAdmin(admin.ModelAdmin):
    pass


@admin.register(AppStore)
class AppStoreModelAdmin(admin.ModelAdmin):
    pass


@admin.register(AppType)
class AppTypeModelAdmin(admin.ModelAdmin):
    pass
