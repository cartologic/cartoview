import os
import uuid
from django.contrib.auth import get_user_model
from django.db import models
from geonode.maps.models import Layer

from .apps import LayerAttachmentsConfig


def get_upload_path(instance, filename) -> str:
    """
    Create a dynamic path for each attachment
    """
    layer_name = instance.layer.name
    feature_id = str(instance.feature_id)
    discard, ext = os.path.splitext(filename)
    basename = uuid.uuid4().urn
    uuid_filename = basename + ext
    upload_folder = os.path.join(LayerAttachmentsConfig.name, 'attachments',
                                 layer_name,
                                 feature_id,
                                 uuid_filename)
    return upload_folder


class LayerAttachment(models.Model):
    """
    A single attachment file that is related to a feature in a vector layer
    """
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, related_name="layer_attachments")
    feature_id = models.CharField(max_length=100)
    file = models.FileField(upload_to=get_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   related_name="layer_attachments")

    def __str__(self):
        return "{} - {}".format(self.layer.name, os.path.basename(self.file.name))

    class Meta:
        ordering = ('-created_at',)
