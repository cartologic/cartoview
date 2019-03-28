# -*- coding: utf-8 -*-
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from cartoview.connections.models import (Server, SimpleAuthConnection,
                                          TokenAuthConnection)


class SimpleAuthConnectionSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = SimpleAuthConnection
        fields = '__all__'


class TokenAuthConnectionSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = TokenAuthConnection
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    operations = serializers.DictField(read_only=False)
    connection = GenericRelatedField({
        SimpleAuthConnection: SimpleAuthConnectionSerializer(),
        TokenAuthConnection: TokenAuthConnectionSerializer()
    })

    class Meta:
        model = Server
        fields = ("id",
                  "created_at",
                  "updated_at",
                  "server_type",
                  "title",
                  "url",
                  "connection",
                  "operations")
