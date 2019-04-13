# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from ..permissions import UserPermission
from ..serializers.user import UserSerializer
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    @action(detail=False, methods=["get"],
            permission_classes=[permissions.IsAuthenticated])
    def current_user(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=200)
