# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions


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

    def validate(self, data):
        # get the password from the data
        username = data.get('username')
        password = data.get('password')
        User = get_user_model()
        user = User(username=username, password=password)
        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)
