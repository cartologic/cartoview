from .views import _resolve_appinstance, _PERMISSION_MSG_MODIFY, _PERMISSION_MSG_VIEW


def can_change_app_instance(function):
    def wrap(request, *args, **kwargs):
        instance_id = kwargs.get('instance_id', None)
        assert instance_id
        _resolve_appinstance(
            request, instance_id, 'base.change_resourcebase',
            _PERMISSION_MSG_MODIFY)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def can_view_app_instance(function):
    def wrap(request, *args, **kwargs):
        instance_id = kwargs.get('instance_id', None)
        assert instance_id
        _resolve_appinstance(request, instance_id,
                             'base.view_resourcebase',
                             _PERMISSION_MSG_VIEW)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
