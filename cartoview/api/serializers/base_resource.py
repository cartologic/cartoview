# -*- coding: utf-8 -*-
from rest_framework import serializers

from cartoview.base_resource.models import BaseModel

from ..fields import TagsListField


class BaseModelSerializer(serializers.ModelSerializer):
    keywords = TagsListField()

    class Meta:
        model = BaseModel
        fields = '__all__'

    def create(self, validated_data):
        keywords = validated_data.pop('keywords', None)
        instance = super(BaseModelSerializer, self).create(validated_data)
        if keywords:
            instance.keywords.set(*keywords)
        return instance

    def update(self, instance, validated_data):
        keywords = validated_data.pop('keywords', None)
        obj = super(BaseModelSerializer, self).update(
            instance, validated_data)
        if keywords:
            obj.keywords.set(*keywords)
        return obj
