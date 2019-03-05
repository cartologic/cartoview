# -*- coding: utf-8 -*-
from abc import ABC, abstractproperty, abstractmethod
from ..auth.base import NoAuthClass


class BaseServer(ABC):
    def __init__(self, base_url, session=NoAuthClass.requests_retry_session()):
        self.url = base_url
        self.session = session

    @abstractmethod
    def get_layers(self):
        return NotImplemented

    @abstractproperty
    def wms_service(self):
        return NotImplemented

    @abstractproperty
    def wms_url(self):
        return NotImplemented

    @abstractproperty
    def rest(self):
        return NotImplemented

    @abstractproperty
    def is_alive(self):
        return NotImplemented
