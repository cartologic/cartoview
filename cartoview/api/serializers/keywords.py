from rest_framework import serializers
from taggit.models import Tag


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
