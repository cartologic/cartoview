from rest_framework import serializers
from cartoview.maps.models import Map
import json
from ..fields import TagsListField


class CenterField(serializers.CharField):

    def to_representation(self, value):
        data = None
        data = json.loads(value)
        return data

    def to_internal_value(self, data):
        if isinstance(data, list):
            return json.dumps(data)
        return data


class MapSerializer(serializers.ModelSerializer):
    center = CenterField()
    owner = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    keywords = TagsListField()

    def create(self, validated_data):
        keywords = validated_data.pop('keywords', None)
        instance = super(MapSerializer, self).create(validated_data)
        if keywords:
            instance.keywords.set(*keywords)
        return instance

    def update(self, instance, validated_data):
        keywords = validated_data.pop('keywords', None)
        instance = super(MapSerializer, self).update(instance, validated_data)
        if keywords:
            instance.keywords.set(*keywords)
        return instance

    class Meta:
        model = Map
        fields = '__all__'
