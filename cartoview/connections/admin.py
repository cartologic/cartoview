# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Server, SimpleAuthConnection, TokenAuthConnection
from .forms import SimpleAuthConnectionForm
from guardian import admin as guardian_admin


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'server_type')
    actions = ['harvest_resources']

    def harvest_resources(self, request, queryset):
        for server in queryset:
            server.handler.harvest()
        self.message_user(
            request, "server resources successfully harvested.")
    harvest_resources.short_description = "Harvest Resources"


@admin.register(SimpleAuthConnection)
class SimpleAuthConnectionAdmin(guardian_admin.GuardedModelAdmin):
    list_display = ('username', 'auth_type')
    form = SimpleAuthConnectionForm


@admin.register(TokenAuthConnection)
class TokenAuthConnectionAdmin(guardian_admin.GuardedModelAdmin):
    list_display = ('prefix', 'token')
