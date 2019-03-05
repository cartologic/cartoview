# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Server, SimpleAuthConnection, TokenAuthConnection


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('server_type', 'title', 'url')


@admin.register(SimpleAuthConnection)
class SimpleAuthConnectionAdmin(admin.ModelAdmin):
    list_display = ('username', 'auth_type')


@admin.register(TokenAuthConnection)
class TokenAuthConnectionAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'token')
