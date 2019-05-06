# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import SiteLogo


@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    list_display = ('site', 'logo')
