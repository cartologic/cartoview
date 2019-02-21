# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from guardian.shortcuts import assign_perm
from taggit.managers import TaggableManager

# Create your models here.

APPS_PERMISSIONS = (
    ('install_app', 'Install App'),
    ('uninstall_app', 'Uninstall App'),
    ('change_state', 'Change App State (active, suspend)'),
)


class AppTypeManager(models.Manager):
    def without_apps_duplication(self):
        return super(AppTypeManager, self).get_queryset().distinct("apps")


@python_2_unicode_compatible
class AppType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    objects = AppTypeManager()

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AppStore(models.Model):
    """
    to store links for cartoview appstores
    """

    SERVER_CHOICES = (
        ("Exchange", "Exchange"),
        ("Geoserver", "Geoserver"),
        ("QGISServer", "QGISServer"),
    )
    name = models.CharField(max_length=256)
    url = models.URLField(verbose_name="App Store URL")
    is_default = models.BooleanField(default=False)
    server_type = models.CharField(
        max_length=256, choices=SERVER_CHOICES, default="Geoserver"
    )

    class Meta:
        ordering = ['-name']

    def as_dict(self):
        return {'name': self.name,
                'id': self.id,
                'url': self.url,
                'is_default': self.is_default,
                'type': self.server_type}

    def __str__(self):
        return self.name


@python_2_unicode_compatible
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

    class Meta:
        ordering = ["order"]
        permissions = APPS_PERMISSIONS

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


@receiver(pre_save, sender=App)
def set_app_order(sender, instance, **kwargs):
    # check if another app have the same order
    count = App.objects.filter(order=instance.order).count()
    # set app correct order
    if instance.order == 0 or count > 1:
        max_order = App.objects.aggregate(
            Max('order'))['order__max']
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
                print(app_permission[0])
                assign_perm(app_permission[0], user, obj=app)
