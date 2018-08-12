# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import abc

from django.utils.translation import ugettext as _
from future import standard_library
from future.utils import with_metaclass
from geonode.utils import resolve_object

from cartoview.app_manager.models import AppInstance

standard_library.install_aliases()

_PERMISSION_MSG_GENERIC = _("You do not have permissions for this Instance.")


def resolve_appinstance(request,
                        appinstanceid,
                        permission='base.change_resourcebase',
                        msg=_PERMISSION_MSG_GENERIC,
                        **kwargs):
    """
    Resolve the document by the provided primary key
    and check the optional permission.
    """
    return resolve_object(
        request,
        AppInstance, {'pk': appinstanceid},
        permission=permission,
        permission_msg=msg,
        **kwargs)


class Thumbnail(with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def create_thumbnail(self):
        """Implement your thumbnail method"""
        pass


class AppsThumbnail(Thumbnail):
    def __init__(self, instance):
        self.instance = instance

    def create_thumbnail(self):
        instance = self.instance
        if not isinstance(instance, AppInstance):
            return
        elif (instance.thumbnail_url is not None or
              instance.thumbnail_url != "") and instance.map is not None:
            parent_app_thumbnail_url = instance.map.get_thumbnail_url()
            instance.thumbnail_url = parent_app_thumbnail_url
            instance.save()


def populate_apps():
    from django.apps import apps
    from django.conf import settings
    apps.populate(settings.INSTALLED_APPS)
