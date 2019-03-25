from abc import ABC, abstractmethod
from functools import lru_cache

import requests
from django.conf import settings
from requests.packages.urllib3.util.retry import Retry

from cartoview.connections import DEFAULT_PROXY_SETTINGS

from .adapters import TimeoutSupportAdapter


class BaseSession(ABC):
    @classmethod
    @abstractmethod
    def get_session(cls, auth_obj):
        return NotImplemented

    @classmethod
    @lru_cache(maxsize=256)
    def get_requests_settings(cls):
        key = "proxy"
        connections_settings = getattr(settings, "CARTOVIEW_CONNECTIONS", {})
        proxy_settings = connections_settings.get(
            key, DEFAULT_PROXY_SETTINGS)
        return proxy_settings

    @classmethod
    @lru_cache(maxsize=256)
    def default_timeout(cls):
        s = cls.get_requests_settings()
        t = s.get('timeout', 10)
        return t

    @classmethod
    @lru_cache(maxsize=256)
    def requests_retry_session(cls, retries=5,
                               backoff_factor=1,
                               status_forcelist=(502, 503, 504),
                               session=None):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            method_whitelist=frozenset(['GET', 'POST', 'PUT', 'DELETE', 'HEAD']))
        adapter = TimeoutSupportAdapter(
            max_retries=retry, timeout=cls.default_timeout())
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session


class NoAuthClass(BaseSession):
    @lru_cache(maxsize=256)
    def get_session(cls, auth_obj):
        return cls.requests_retry_session()
