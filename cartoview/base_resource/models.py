import os
from datetime import datetime

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class TaggedResource(TaggedItemBase):
    content_object = models.ForeignKey(
        'BaseModel', on_delete=models.SET_NULL, null=True,
        related_name='tagged_items')


def thumbnail_path(instance, filename):
    today = datetime.now()
    date_as_path = today.strftime("%Y/%m/%d")
    return '/'.join(['thumbnails', str(instance.id), date_as_path, filename])


def featured_image(instance, filename):
    today = datetime.now()
    date_as_path = today.strftime("%Y/%m/%d")
    return '/'.join(['featured_images', str(instance.id), date_as_path,
                     filename])


class BaseModel(models.Model):
    title = models.CharField(max_length=255, default=_("No title Provided"))
    description = models.TextField(
        null=True, blank=True, default=_("No Description Provided"))
    abstract = models.TextField(
        null=True, blank=True, default=_("No Abstract Provided"))
    featured_image = models.ImageField(
        upload_to=thumbnail_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(
        upload_to=thumbnail_path, null=True, blank=True)
    keywords = TaggableManager(through=TaggedResource, blank=True)

    class Meta:
        ordering = ('title', '-created_at', '-updated_at')


@receiver(post_delete, sender=BaseModel)
def photo_post_delete_handler(sender, **kwargs):
    instance = kwargs['instance']
    file_objs = [instance.featured_image, instance.thumbnail]
    for file_obj in file_objs:
        if not file_obj:
            continue
        storage, path = getattr(file_obj, 'storage'), getattr(file_obj, 'path')
        if path and os.path.exists(path):
            storage.delete(path)
