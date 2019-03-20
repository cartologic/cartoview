# -*- coding: utf-8 -*-
from abc import ABC, abstractproperty, abstractmethod
from ..auth.base import NoAuthClass
from cartoview.connections.models import Server, SimpleAuthConnection, TokenAuthConnection


class BaseServer(ABC):
    def __init__(self, base_url, server_id):
        self.url = base_url
        self.server = Server.objects.prefetch_related(
            'connection').get(id=server_id)

    @property
    def session(self):
        conn = self.server.connection
        if conn:
            return conn.session
        else:
            return NoAuthClass.requests_retry_session()

    @property
    def extra_kwargs(self):
        extra_kwargs = {}
        if self.erver.connection:
            auth_obj = self.server.connection
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
    def rest(self):
        return NotImplemented

    @abstractproperty
    def is_alive(self):
        return NotImplemented
