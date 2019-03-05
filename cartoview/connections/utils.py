from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from cartoview.log_handler import get_logger

from .exceptions import ConnectionTypeException

logger = get_logger(__name__)


def urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip('/'), args))


def get_module_class(name):
    return name.rsplit('.', 1)


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
