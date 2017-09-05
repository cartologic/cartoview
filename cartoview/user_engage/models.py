from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
from django.contrib.gis.db import models
from django.conf import settings
UserModel = settings.AUTH_USER_MODEL


class BasicModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserModel, related_name="engage_%(class)s")
    identifier = models.CharField(max_length=256)

    class Meta(object):
        abstract = True


class Comment(BasicModel):
    comment = models.TextField()

    def __unicode__(self):
        return self.comment


class Rating(BasicModel):
    rate = models.PositiveSmallIntegerField()


class Image(BasicModel):
    image = models.ImageField(upload_to="user_engage/images/")
    title = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.title
