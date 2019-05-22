# -*- coding: utf-8 -*-
from cartoview.connections.tasks import (delete_invalid_resources,
                                         harvest_task, update_server_resources,
                                         validate_server_resources)
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from guardian import admin as guardian_admin

from .forms import SimpleAuthConnectionForm
from .models import Server, SimpleAuthConnection, TokenAuthConnection


class ServerAdminInline(GenericTabularInline):
    model = Server


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'server_type')
    actions = ['harvest_resources', 'update_resources',
               'validate_resources', 'delete_invalid']

    def harvest_resources(self, request, queryset):
        for server in queryset:
            harvest_task.delay(server_id=server.id)
        self.message_user(
            request, "server resources will be harvested.")
    harvest_resources.short_description = "Harvest Resources"

    def update_resources(self, request, queryset):
        for server in queryset:
            update_server_resources.delay(server_id=server.id)
        self.message_user(
            request, "server resources will be Updated")
    update_resources.short_description = "Update Resources"

    def validate_resources(self, request, queryset):
        for server in queryset:
            validate_server_resources.delay(server_id=server.id)
        self.message_user(
            request, "server resources will be Validated")
    validate_resources.short_description = "Validate Resources"

    def delete_invalid(self, request, queryset):
        for server in queryset:
            delete_invalid_resources.delay(server_id=server.id)
        self.message_user(
            request, "server resources will be Validated")
    delete_invalid.short_description = "Delete Invalid Resources"


@admin.register(SimpleAuthConnection)
class SimpleAuthConnectionAdmin(guardian_admin.GuardedModelAdmin):
    list_display = ('username', 'auth_type')
    form = SimpleAuthConnectionForm
    inlines = [ServerAdminInline, ]


@admin.register(TokenAuthConnection)
class TokenAuthConnectionAdmin(guardian_admin.GuardedModelAdmin):
    list_display = ('prefix', 'token')
    inlines = [ServerAdminInline, ]
