# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from cartoview import __version__
from cartoview.app_manager.models import App
from cartoview.site_management.models import SiteLogo
from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from future import standard_library


standard_library.install_aliases()


def apps(request):
    return {'apps': App.objects.all().order_by('order')}


def cartoview_processor(request):
    defaults = {
        # TODO: use rest api instead!
        'apps': App.objects.all().order_by('order'),
        # TODO: fixme: return version with PEP8 standard
        'CARTOVIEW_VERSION': __version__,
        'APPS_MENU': settings.APPS_MENU,
    }
    return defaults


def site_logo(request):
    try:
        logo = get_object_or_404(SiteLogo, site=Site.objects.get_current())
        return {'site_logo': logo}
    except BaseException:
        return {'site_logo': None}
