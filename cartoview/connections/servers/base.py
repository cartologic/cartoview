# -*- coding: utf-8 -*-
from abc import ABC, abstractproperty, abstractmethod
from ..auth.base import NoAuthClass
from cartoview.connections.models import Server


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
