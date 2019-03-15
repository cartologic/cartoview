# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class AppPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        permitted = False
        if request.method in ("GET", "OPTIONS"):
            permitted = True
        elif request.method in ("PATCH", "PUT"):
            permitted = request.user.has_perm('change_state', obj)
        elif request.method == "POST":
            permitted = (request.user.has_perm('install_app', obj) or
                         request.user.has_perm('uninstall_app', obj))
        elif request.method == "GET":
            permitted = True
        print(permitted)
        return permitted


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user and request.user.is_superuser:
            return True
        elif obj == request.user:
            return True
        return False

    def has_permission(self, request, view):
        return True
