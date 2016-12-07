from django.contrib import admin
from .models import AppStore


# Register your models here.
@admin.register(AppStore)
class AppStoreAdmin(admin.ModelAdmin):
    pass
