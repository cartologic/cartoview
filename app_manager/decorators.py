from .exceptions import AppAlreadyInstalledException
from django.conf import settings


def restart_enabled(func):
    def wrap(*args, **kwargs):
        if not getattr(settings, "CARTOVIEW_TEST", False):
            return func(*args, **kwargs)
    return wrap


def rollback_on_failure(func):
    def wrap(*args, **kwargs):
        this = args[0]
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            if not isinstance(e, AppAlreadyInstalledException):
                if hasattr(this, '_rollback'):
                    this._rollback()
                raise e
    return wrap
