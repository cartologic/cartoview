from django.contrib import admin
from .models import Map
# Register your models here.


@admin.register(Map)
class MapModelAdmin(admin.ModelAdmin):
    pass
