# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class PasswordField(serializers.CharField):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return make_password(data)


class UserSerializer(serializers.ModelSerializer):
    password = PasswordField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'date_joined', 'groups', 'password')
