# -*- coding: utf-8 -*-
from rest_framework import permissions


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
