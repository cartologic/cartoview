# -*- coding: utf-8 -*-
from rest_framework import serializers

from cartoview.app_manager.models import App, AppInstance, AppStore, AppType


class AppTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppType
        fields = '__all__'


class AppStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppStore
        fields = '__all__'


class AppSerializer(serializers.ModelSerializer):
    installed_by = serializers.StringRelatedField(many=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=AppType.objects.all(), many=True,
        allow_null=True)
    store = serializers.PrimaryKeyRelatedField(
        queryset=AppStore.objects.all(), many=False,
        allow_null=True)

    class Meta:
        model = App
        fields = '__all__'


class AppInstanceSerializer(serializers.ModelSerializer):
    map_url = serializers.CharField(read_only=True)

    class Meta:
        model = AppInstance
        fields = '__all__'
