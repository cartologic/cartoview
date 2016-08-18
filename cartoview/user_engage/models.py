from django.contrib.gis.db import models
from django.conf import settings
UserModel = settings.AUTH_USER_MODEL

class BasicModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserModel, related_name="engage_%(class)s")
    identifier = models.CharField(max_length=256)

    class Meta:
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