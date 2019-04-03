# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractproperty
from functools import lru_cache

from django.contrib.auth import get_user_model

from cartoview.connections.models import (Server, SimpleAuthConnection,
                                          TokenAuthConnection)
from cartoview.connections.utils import get_handler_class_handler


class BaseServer(ABC):
    def __init__(self, base_url, server_id, user_id=None):
        self.url = base_url
        self.server = Server.objects.prefetch_related(
            'connection').get(id=server_id)
        USER = get_user_model()
        if user_id:
            self.user = USER.objects.get(id=user_id)
        else:
            self.user = USER.objects.filter(is_superuser=True).first()

    @property
    @lru_cache(maxsize=256)
    def session(self):
        conn = self.server.connection
        if conn:
            return conn.session
        else:
            return get_handler_class_handler("NoAuth").requests_retry_session()

    @property
    def extra_kwargs(self):
        extra_kwargs = {}
        if self.server.connection:
            auth_obj = self.server.connection
            if auth_obj:
                if isinstance(self.server.connection, SimpleAuthConnection):
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
