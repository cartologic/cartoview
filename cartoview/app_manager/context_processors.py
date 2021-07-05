# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf import settings
from future import standard_library
from geonode.groups.models import Group
from geonode.maps.models import Layer, Map
from geonode.people.models import Profile
from geonode.version import get_version
from guardian.shortcuts import get_objects_for_user

from cartoview import __version__
from cartoview.app_manager.models import App, AppInstance

standard_library.install_aliases()


def apps(request):
    return {'apps': App.objects.all().order_by('order')}


def cartoview_processor(request):
    permitted = get_objects_for_user(request.user,
                                     'base.view_resourcebase')
    cartoview_counters = {
        "apps": App.objects.count(),
        "app_instances": AppInstance.objects.filter(id__in=permitted).count(),
        "maps": Map.objects.filter(id__in=permitted).count(),
        "layers": Layer.objects.filter(id__in=permitted).count(),
        "users": Profile.objects.exclude(username="AnonymousUser").count(),
        "groups": Group.objects.exclude(name="anonymous").count()
    }

    defaults = {
        'apps': App.objects.all().order_by('order'),
        'CARTOVIEW_VERSION': get_version(list(__version__)),
        'APPS_MENU': settings.APPS_MENU,
        'apps_instance_count': AppInstance.objects.all().count(),
        "cartoview_counters": cartoview_counters,
        'instances': AppInstance.objects.all().order_by('app__order')[:5]
    }
    return defaults
