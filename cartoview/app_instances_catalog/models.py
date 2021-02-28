from django.db import models
from model_utils.managers import InheritanceManager


class AppInstance(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    abstract = models.TextField(
        max_length=2000,
        null=True,
        blank=True
    )
    config = models.JSONField(
        null=True,
        blank=True
    )

    # model_utils InheritanceManager
    objects = InheritanceManager()
