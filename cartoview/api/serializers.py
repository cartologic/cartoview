# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers

from cartoview.app_manager.models import App, AppStore, AppType


class AppTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppType
        fields = '__all__'


class AppStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppStore
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'date_joined', 'groups', 'password')


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
