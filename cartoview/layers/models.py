from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.urls import reverse_lazy

from cartoview.connections.models import Server
from cartoview.base_resource.models import BaseModel
from .validators import validate_projection


class BaseLayer(models.Model):
    name = models.CharField(max_length=255)
    bounding_box = ArrayField(models.DecimalField(
        max_digits=30,
        decimal_places=15,
        blank=True,
        null=True), size=4, null=False, blank=False)
    projection = models.CharField(
        max_length=30,
        blank=False,
        null=False, validators=[validate_projection, ])
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name='layers')
    valid = models.BooleanField(default=True)

    @property
    def server_type(self):
        return self.server.server_type

    @property
    def server_url(self):
        if self.server:
            return self.server.url
        return None

    @property
    def server_proxy(self):
        return '{}?url='.format(reverse_lazy('api:server_proxy',
                                             args=(self.server.pk,)))

    @property
    def layer_type(self):
        return self.server.resources_type

    class Meta:
        abstract = True
        unique_together = (("name", "server"),)


class Layer(BaseModel, BaseLayer):
    extra = JSONField()

    def __str__(self):
        return "{}({})".format(self.name, self.layer_type)
