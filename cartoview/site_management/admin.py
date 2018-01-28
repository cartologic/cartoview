from django.contrib import admin
from .models import SiteLogo
# Register your models here.


@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    list_display = ('site', 'logo')
