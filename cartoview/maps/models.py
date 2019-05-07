import jsonfield
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from cartoview.base_resource.models import BaseModel
from cartoview.fields import ListField
from cartoview.layers.models import Layer
from cartoview.layers.validators import validate_projection
from cartoview.validators import ListValidator


class Map(BaseModel):
    site = models.ForeignKey(Site, related_name='site_maps',
                             on_delete=models.CASCADE, null=True, blank=True)
    bounding_box = ListField(null=True, blank=True, default=[0, 0, 0, 0],
                             validators=[ListValidator(min_length=4,
                                                       max_length=4), ])
    projection = models.CharField(
        max_length=30,
        blank=False,
        null=False, validators=[validate_projection, ], default="EPSG:3857")
    center = ListField(null=False, blank=False, default=[0, 0], validators=[
                       ListValidator(min_length=2, max_length=2), ])
    constrain_rotation = models.BooleanField(default=True)
    enable_rotation = models.BooleanField(default=True)
    max_zoom = models.IntegerField(default=28, validators=[
        MaxValueValidator(28),
        MinValueValidator(0)
    ])
    min_zoom = models.IntegerField(default=0, validators=[
        MaxValueValidator(28),
        MinValueValidator(0)
    ])
    zoom_factor = models.IntegerField(default=2, validators=[
        MaxValueValidator(28),
        MinValueValidator(1)
    ])
    zoom = models.FloatField(default=6, validators=[
        MaxValueValidator(28),
        MinValueValidator(1)
    ])
    rotation = models.IntegerField(null=False, blank=False, default=0)
    layers = models.ManyToManyField(Layer, blank=True)
    render_options = jsonfield.JSONField(default=dict, null=False, blank=True)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="maps",
        blank=True, null=True)

    def __str__(self):
        return self.title
