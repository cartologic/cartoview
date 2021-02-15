# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import abc

from django.utils.translation import ugettext as _
from future import standard_library
from future.utils import with_metaclass

standard_library.install_aliases()

_PERMISSION_MSG_GENERIC = _("You do not have permissions for this Instance.")


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
        instance_map = getattr(instance, 'related_map', instance.map)
        if instance_map:
            instance.thumbnail_url = instance_map.get_thumbnail_url()
            instance.save()


def populate_apps():
    from django.apps import apps
    from django.conf import settings
    apps.populate(settings.INSTALLED_APPS)
