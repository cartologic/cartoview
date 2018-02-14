from .utils import resolve_appinstance
from django.utils.translation import ugettext as _

PERMISSION_MSG_DELETE = _("You are not permitted to delete this Instance")
PERMISSION_MSG_GENERIC = _("You do not have permissions for this Instance.")
PERMISSION_MSG_MODIFY = _("You are not permitted to modify this Instance")
PERMISSION_MSG_METADATA = _(
    "You are not permitted to modify this Instance's metadata")
PERMISSION_MSG_VIEW = _("You are not permitted to view this Instance")


def can_change_app_instance(function):
    def wrap(request, *args, **kwargs):
        instance_id = kwargs.get('instance_id', None)
        assert instance_id
        resolve_appinstance(
            request, instance_id, 'base.change_resourcebase',
            PERMISSION_MSG_MODIFY)
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def can_view_app_instance(function):
    def wrap(request, *args, **kwargs):
        instance_id = kwargs.get('instance_id', None)
        assert instance_id
        resolve_appinstance(request, instance_id,
                            'base.view_resourcebase',
                            PERMISSION_MSG_VIEW)
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
