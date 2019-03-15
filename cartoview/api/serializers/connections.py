# -*- coding: utf-8 -*-
from rest_framework import serializers

from cartoview.connections.models import (Server, SimpleAuthConnection,
                                          TokenAuthConnection)


class AuthField(serializers.RelatedField):
    def to_representation(self, value):
        data = None
        # NOTE: only the owner of the connection can use it
        user = self.context['request'].user
        if user == value.owner:
            if isinstance(value, SimpleAuthConnection):
                s = SimpleAuthConnectionSerializer(value)
                data = s.data
                data.update({"class": SimpleAuthConnection.__name__})
            elif isinstance(value, TokenAuthConnection):
                s = TokenAuthConnectionSerializer(value)
                data = s.data
                data.update({"class": TokenAuthConnection.__name__})
        return data


class ServerSerializer(serializers.ModelSerializer):
    connection = AuthField(read_only=True)

    class Meta:
        model = Server
        fields = ("id",
                  "created_at",
                  "updated_at",
                  "server_type",
                  "title",
                  "url",
                  "connection")


class SimpleAuthConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleAuthConnection
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True, 'required': False}
        }


class TokenAuthConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenAuthConnection
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True, 'required': False}
        }
