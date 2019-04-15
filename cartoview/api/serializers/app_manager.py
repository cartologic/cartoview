# -*- coding: utf-8 -*-
from rest_framework import serializers

from cartoview.app_manager.models import (App, AppInstance, AppStore, AppType,
                                          Bookmark)
from cartoview.maps.models import Map

from .base_resource import BaseModelSerializer


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


class BookmarkSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(many=False)

    class Meta:
        model = Bookmark
        fields = '__all__'


class AppInstanceSerializer(BaseModelSerializer):
    map_url = serializers.CharField(read_only=True)
    app_map = serializers.PrimaryKeyRelatedField(queryset=Map.objects.all())
    owner = serializers.StringRelatedField(many=False, read_only=False)
    bookmarks = BookmarkSerializer(many=True)

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        bookmarks_data = validated_data.pop('bookmarks', [])
        created_bookmarks = []
        appinstance = super(AppInstanceSerializer, self).create(validated_data)
        for bookmark_data in bookmarks_data:
            bookmark = Bookmark.objects.create(owner=user, **bookmark_data)
            created_bookmarks.append(bookmark)
        if len(created_bookmarks) > 0:
            appinstance.bookmarks.set(created_bookmarks)
        return appinstance

    def update(self, instance, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        bookmarks_data = validated_data.pop('bookmarks', [])
        created_bookmarks = []
        appinstance = super(AppInstanceSerializer, self).update(
            instance, validated_data)
        for bookmark_data in bookmarks_data:
            bookmark = Bookmark.objects.create(owner=user, **bookmark_data)
            created_bookmarks.append(bookmark)
        if len(created_bookmarks) > 0:
            appinstance.bookmarks.set(created_bookmarks)
        return appinstance

    class Meta:
        model = AppInstance
        fields = '__all__'
