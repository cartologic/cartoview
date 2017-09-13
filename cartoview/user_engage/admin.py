from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import *
from django.contrib import admin

from .models import Comment, Image, Rating

# Register your models here.
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Rating)
