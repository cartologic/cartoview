# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class AppPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        permitted = True
        if request.method == "POST" and view.name == "Install":
            permitted = request.user.has_perm('install_app')
        return permitted

    def has_object_permission(self, request, view, obj):
        permitted = False
        if request.user.is_superuser or request.method in SAFE_METHODS:
            permitted = True
        elif request.method in ("PATCH", "PUT"):
            permitted = request.user.has_perm('change_state', obj)
        elif request.method == "POST":
            permitted = request.user.has_perm('install_app')
        elif request.method == "DELETE":
            permitted = request.user.has_perm('uninstall_app', obj)
        return permitted


class BaseObjectPermissions(permissions.DjangoObjectPermissions):
    authenticated_users_only = False
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


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


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or \
                    (request.user and request.user.is_superuser)
