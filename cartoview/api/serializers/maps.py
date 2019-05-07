from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers

from cartoview.fields import ListSerializerField
from cartoview.maps.models import Map

from .base_resource import BaseModelSerializer


class MapSerializer(BaseModelSerializer):
    center = ListSerializerField()
    bounding_box = ListSerializerField(required=False)
    owner = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        user = None
        site = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            site = get_current_site(request)
            user = request.user
        instance = super(MapSerializer, self).create(validated_data)
        instance.owner = user
        instance.site = site
        instance.save()
        return instance

    def update(self, instance, validated_data):
        user = None
        site = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            site = get_current_site(request)
            user = request.user
        instance = super(MapSerializer, self).update(
            instance, validated_data)
        if not instance.owner:
            instance.owner = user
        if not instance.site:
            instance.site = site
        instance.save()
        return instance

    class Meta:
        model = Map
        fields = '__all__'
