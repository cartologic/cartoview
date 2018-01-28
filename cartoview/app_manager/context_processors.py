# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from builtins import *

from cartoview.app_manager.models import App, AppInstance
from cartoview.site_management.models import SiteLogo
from django.conf import settings
from geonode.version import get_version
from cartoview import __version__
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from future import standard_library

standard_library.install_aliases()


def apps(request):
    return {'apps': App.objects.all().order_by('order')}


def cartoview_processor(request):
    defaults = {
        'apps': App.objects.all().order_by('order'),
        'CARTOVIEW_VERSION': get_version(__version__),
        'APPS_MENU': settings.APPS_MENU,
        'apps_instance_count': AppInstance.objects.all().count(),
        'instances': AppInstance.objects.all().order_by('app__order')[:5]
    }
    return defaults


def site_logo(request):
    try:
        logo = get_object_or_404(SiteLogo, site=Site.objects.get_current())
        return {'site_logo': logo}
    except BaseException:
        return {'site_logo': None}
