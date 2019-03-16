# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from ..serializers.user import UserSerializer
from ..permissions import UserPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)
