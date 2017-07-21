from django.contrib import admin

from models import Comment, Image, Rating

# Register your models here.
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Rating)
