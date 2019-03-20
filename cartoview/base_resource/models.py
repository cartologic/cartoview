from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class BaseModel(models.Model):
    title = models.CharField(max_length=255, default=_("No title Provided"))
    description = models.TextField(
        null=True, blank=True, default=_("No Description Provided"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title', '-created_at', '-updated_at')
