import json

from geonode.layers.models import Layer
from rest_framework import serializers

from .models import LayerAttachment
from .apps import LayerAttachmentsConfig


class LayerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the layers that have attachments
    """
    layer_attributes = serializers.SerializerMethodField()

    def get_layer_attributes(self, obj):
        config = obj.attribute_config()
        return config["getFeatureInfo"]["fields"]

    class Meta:
        model = Layer
        fields = ('id', 'name', 'title', 'typename', 'ows_url', 'date', 'thumbnail_url', 'layer_attributes')


class AttachmentManagerInfoSerializer(serializers.Serializer):
    """
    Serializer class for the data collection app info
    """
    name = serializers.CharField(required=False, read_only=True)
    verbose_name = serializers.CharField(required=False, read_only=True)
    title = serializers.CharField(required=False, read_only=True)
    description = serializers.CharField(required=False, read_only=True)
    author = serializers.CharField(required=False, read_only=True)
    author_website = serializers.CharField(required=False, read_only=True)
    help_url = serializers.CharField(required=False, read_only=True)
    licence = serializers.CharField(required=False, read_only=True)
    version = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = LayerAttachmentsConfig


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the attachments
    """
    layer = serializers.PrimaryKeyRelatedField(queryset=Layer.objects.all())
    layer_name = serializers.ReadOnlyField(source='layer.name')
    layer_typename = serializers.ReadOnlyField(source='layer.typename')
    created_by = serializers.ReadOnlyField(source='created_by.username')
    size = serializers.ReadOnlyField(source='file.size')

    class Meta:
        model = LayerAttachment
        fields = (
        'id', 'file', 'layer', 'layer_name', 'layer_typename', 'feature_id', 'created_by', 'created_at', 'updated_at',
        'size')
