from django.conf import settings
from django.utils.translation import ugettext as _

from .exceptions import AppAlreadyInstalledException

PERMISSION_MSG_DELETE = _("You are not permitted to delete this Instance")
PERMISSION_MSG_GENERIC = _("You do not have permissions for this Instance.")
PERMISSION_MSG_MODIFY = _("You are not permitted to modify this Instance")
PERMISSION_MSG_METADATA = _(
    "You are not permitted to modify this Instance's metadata")
PERMISSION_MSG_VIEW = _("You are not permitted to view this Instance")


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
