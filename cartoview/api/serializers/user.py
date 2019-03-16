# -*- coding: utf-8 -*-
import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


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

    def validate_password(self, value):
        User = get_user_model()
        user = User(**self.initial_data)
        password = self.initial_data['password']
        try:
            validators.validate_password(password, user=user)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'date_joined', 'groups', 'password')
