from django.contrib import admin
from myapp.models import Song

class SongAdmin(admin.ModelAdmin):
    pass

admin.site.register(Song, SongAdmin)

