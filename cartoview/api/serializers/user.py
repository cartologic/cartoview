# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers


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
