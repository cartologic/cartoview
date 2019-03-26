# -*- coding: utf-8 -*-
from functools import lru_cache
from urllib.parse import parse_qsl, unquote_plus, urlparse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from cartoview.log_handler import get_logger

from . import SUPPORTED_SERVERS
from .exceptions import ConnectionTypeException

logger = get_logger(__name__)


class URL(object):
    def __init__(self, url):
        parts = urlparse(url)
        _query = frozenset(parse_qsl(parts.query))
        _path = unquote_plus(parts.path)
        parts = parts._replace(query=_query, path=_path)
        self.parts = parts

    def __eq__(self, other):
        return self.parts == other.parts

    @classmethod
    def compare_netloc(cls, source_url, target_url):
        source = URL(source_url)
        target = URL(target_url)
        return source.parts.netloc == target.parts.netloc

    def __hash__(self):
        return hash(self.parts)


def urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip('/'), args))


def get_module_class(name):
    return name.rsplit('.', 1)


def get_server_by_value(value):
    server = None
    for s in SUPPORTED_SERVERS:
        if s.value == value:
            server = s
            break
    return server


@lru_cache(maxsize=256)
def get_handler_class_handler(handler_key, server=False):
    key = "server_handlers" if server else "connection_handlers"
    connections_settings = getattr(settings, "CARTOVIEW_CONNECTIONS", {})
    handlers_dict = connections_settings.get(
        key, None)
    if not handlers_dict:
        raise ImproperlyConfigured(
            _("CARTOVIEW_CONNECTIONS Improperly Configured"))
    if handler_key not in handlers_dict.keys():
        raise ConnectionTypeException(
            "Can\'t Find Proper Connection Handler")
    try:

        handler_module, handler_name = get_module_class(
            handlers_dict.get(handler_key))
        mod = __import__(handler_module, fromlist=[handler_name, ])
        handler = getattr(mod, handler_name)
    except ImportError as e:
        logger.error(e)
    return handler
