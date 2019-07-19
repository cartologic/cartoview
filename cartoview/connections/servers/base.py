# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractproperty
from functools import lru_cache

from cartoview.connections.models import (Server, SimpleAuthConnection,
                                          TokenAuthConnection)
from cartoview.connections.utils import HandlerManager
from django.contrib.auth import get_user_model


class BaseServer(ABC):
    def __init__(self, base_url, server_id, user_id=None):
        self.url = base_url
        self.server = Server.objects.get(id=server_id)
        self.user_id = user_id
        self.user = None
        if user_id:
            USER = get_user_model()
            self.user = USER.objects.get(id=user_id)

    @property
    @lru_cache(maxsize=256)
    def session(self):
        handler_manager = HandlerManager("NoAuth")
        conn = self.get_connection_auth()
        if conn:
            return conn.credentials.session
        return handler_manager.anonymous_session

    def get_connection_auth(self):
        conn = None
        connections = self.server.connections
        if connections.count() > 0:
            user_con = connections.filter(owner=self.user).first()
            if user_con:
                return user_con
        return conn

    @property
    def extra_kwargs(self):
        extra_kwargs = {}
        if self.server.connections:
            conn = self.get_connection_auth()
            if conn and conn.credentials:
                auth_obj = conn.credentials
                if isinstance(conn.credentials, SimpleAuthConnection):
                    extra_kwargs.update(
                        {'username': auth_obj.username,
                         'password': auth_obj.password})
                elif isinstance(self.server.connection, TokenAuthConnection):
                    headers = {}
                    if auth_obj.prefix and auth_obj.prefix != "":
                        headers['Authorization'] = "{} {}".format(auth_obj.prefix,
                                                                  auth_obj.token)
                    else:
                        headers['Authorization'] = "{}".format(auth_obj.token)
                    extra_kwargs.update({'headers': headers})
        return extra_kwargs

    @abstractmethod
    def get_layers(self):
        return NotImplemented

    @abstractmethod
    def harvest(self):
        return NotImplemented

    @abstractproperty
    def is_alive(self):
        return NotImplemented

    @abstractproperty
    def operations(self):
        return NotImplemented
