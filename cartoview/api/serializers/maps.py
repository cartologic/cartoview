from rest_framework import serializers

from cartoview.fields import ListSerializerField
from cartoview.maps.models import Map

from .base_resource import BaseModelSerializer


class MapSerializer(BaseModelSerializer):
    center = ListSerializerField()
    bounding_box = ListSerializerField(required=False)
    owner = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Map
        fields = '__all__'
