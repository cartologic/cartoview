from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.urls import reverse_lazy

from cartoview.connections.models import Server

from .validators import validate_projection


class BaseLayer(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    bounding_box = ArrayField(models.DecimalField(
        max_digits=30,
        decimal_places=15,
        blank=True,
        null=True), size=4, null=False, blank=False)
    projection = models.CharField(
        max_length=30,
        blank=False,
        null=False, validators=[validate_projection, ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name='layers')
    valid = models.BooleanField(default=True)
    services = ArrayField(models.CharField(
        max_length=15,
        blank=False,
        null=False), size=4, null=False, blank=False, default=[])

    @property
    def server_type(self):
        return self.server.server_type

    @property
    def server_url(self):
        return '{}?url='.format(reverse_lazy('api:server_proxy',
                                             args=(self.server.pk,)))

    class Meta:
        abstract = True
        ordering = ('-name', '-created_at', '-updated_at')
        unique_together = (("name", "server"),)


class Layer(BaseLayer):
    extra = JSONField()

    def __str__(self):
        return self.name
