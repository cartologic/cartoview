# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from ..serializers.user import UserSerializer
from ..permissions import UserPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def perform_create(self, serializer):
        serializer.validated_data['password'] = make_password(
            serializer.validated_data['password'])
        serializer.save()

    def perform_update(self, serializer):
        data = serializer.validated_data
        if data.get('password', None):
            serializer.validated_data['password'] = make_password(
                serializer.validated_data['password'])
        serializer.save()
