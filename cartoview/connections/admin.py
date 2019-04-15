# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Server, SimpleAuthConnection, TokenAuthConnection
from .forms import SimpleAuthConnectionForm
from guardian import admin as guardian_admin
from cartoview.connections.tasks import (harvest_task, update_server_resources,
                                         validate_server_resources,
                                         delete_invalid_resources)


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'server_type')
    actions = ['harvest_resources', 'update_resources',
               'validate_resources', 'delete_invalid']

    def harvest_resources(self, request, queryset):
        for server in queryset:
            harvest_task.delay(server_id=server.id)
        self.message_user(
            request, "server resources successfully harvested.")
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


@admin.register(TokenAuthConnection)
class TokenAuthConnectionAdmin(guardian_admin.GuardedModelAdmin):
    list_display = ('prefix', 'token')
