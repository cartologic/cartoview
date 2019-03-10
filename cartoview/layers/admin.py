from django.contrib import admin
from .models import Layer
# Register your models here.


@admin.register(Layer)
class LayerAdminModel(admin.ModelAdmin):
    pass
