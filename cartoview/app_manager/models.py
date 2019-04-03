# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm
from taggit.managers import TaggableManager

from cartoview.base_resource.models import BaseModel
from cartoview.maps.models import Map

APPS_PERMISSIONS = (
    ("install_app", _("Install App")),
    ("uninstall_app", _("Uninstall App")),
    ("change_state", _("Change App State (active, suspend)")),
)


class AppTypeManager(models.Manager):
    def without_apps_duplication(self):
        return super(AppTypeManager, self).get_queryset().distinct("apps")


class AppType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    objects = AppTypeManager()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AppStore(models.Model):
    """
    to store links for cartoview appstores
    """

    SERVER_CHOICES = (
        ("Exchange", _("Exchange")),
        ("Geoserver", _("Geoserver")),
        ("QGISServer", _("QGISServer")),
    )
    name = models.CharField(max_length=256)
    url = models.URLField(verbose_name="App Store URL")
    is_default = models.BooleanField(default=False)
    server_type = models.CharField(
        max_length=256, choices=SERVER_CHOICES, default="Geoserver"
    )

    class Meta:
        ordering = ["-name"]

    def as_dict(self):
        return {"name": self.name,
                "id": self.id,
                "url": self.url,
                "is_default": self.is_default,
                "type": self.server_type}

    def __str__(self):
        return self.name


class App(models.Model):
    name = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    license = models.CharField(max_length=200, null=True, blank=True)
    tags = TaggableManager()
    date_installed = models.DateTimeField(
        "Date Installed", auto_now_add=True, null=True
    )
    installed_by = models.ForeignKey(
        get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    single_instance = models.BooleanField(
        default=False, null=False, blank=False)
    category = models.ManyToManyField(
        AppType, related_name="apps", blank=True)
    status = models.CharField(
        max_length=100, blank=False, null=False, default="Alpha")
    app_img_url = models.TextField(max_length=1000, blank=True, null=True)
    version = models.CharField(max_length=10)
    store = models.ForeignKey(
        AppStore, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.IntegerField(default=0, unique=True)
    default_config = JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        permissions = APPS_PERMISSIONS

    def __str__(self):
        return self.title


class AppInstance(BaseModel):
    app_map = models.ForeignKey(
        Map, related_name="app_instances", on_delete=models.CASCADE)
    app = models.ForeignKey(
        App, related_name="instances", on_delete=models.CASCADE)

    config = JSONField(default=None, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def map_url(self):
        if self.app_map:
            return reverse_lazy("api:maps-map_json",
                                kwargs={"pk": self.app_map.pk})
        return None


@receiver(pre_save, sender=App)
def set_app_order(sender, instance, **kwargs):
    # check if another app have the same order
    count = App.objects.filter(order=instance.order).count()
    # set app correct order
    if instance.order == 0 or count > 1:
        max_order = App.objects.aggregate(
            Max("order"))["order__max"]
        if max_order:
            instance.order = max_order+1
        else:
            instance.order = 1


@receiver(post_save, sender=App)
def set_app_default_permissions(sender, **kwargs):
    app, created = kwargs["instance"], kwargs["created"]
    users = get_user_model().objects.filter(is_superuser=True,)
    if app.installed_by:
        users = users.union(get_user_model().objects.filter(
            username=app.installed_by.username))
    users = users.exclude(username=settings.ANONYMOUS_USER_NAME)
    if created:
        for user in users:
            for app_permission in APPS_PERMISSIONS:
                assign_perm(app_permission[0], user, obj=app)


@receiver(post_save, sender=AppInstance)
@receiver(post_delete, sender=AppInstance)
def invalidate_appinstance_cache(sender, instance, **kwargs):
    cache.delete("appinstances")


@receiver(post_save, sender=get_user_model())
def add_default_user_group(sender, instance, **kwargs):
    created = kwargs.get("created")
    if created:
        public_group = Group.objects.get(name="public")
        instance.groups.add(public_group)
