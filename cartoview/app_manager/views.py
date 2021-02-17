# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import abc
import json
import os

from cartoview.log_handler import get_logger
from django.conf import settings
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F, Max, Min
from django.forms.utils import ErrorList
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from future import standard_library
from future.utils import with_metaclass
from geonode.base.forms import CategoryForm
from geonode.base.models import TopicCategory
from geonode.people.forms import ProfileForm
from geonode.security.views import _perms_info_json
from geonode.utils import build_social_links
from guardian.shortcuts import get_perms

from .decorators import PERMISSION_MSG_VIEW
from .installer import AppInstaller
from .models import App
from .utils import AppsThumbnail

logger = get_logger(__name__)

standard_library.install_aliases()

current_folder, filename = os.path.split(os.path.abspath(__file__))
temp_dir = os.path.join(current_folder, 'temp')
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


def get_apps_names():
    apps = []
    if os.path.exists(settings.APPS_DIR):
        apps = [
            n for n in os.listdir(settings.APPS_DIR)
            if os.path.isdir(os.path.join(settings.APPS_DIR, n))
        ]
    return apps


def installed_apps():
    from .models import App
    apps = App.objects.filter().order_by('order')
    return apps


@staff_member_required
def manage_apps(request):
    from cartoview.version import get_backward_compatible, get_current_version
    from pkg_resources import parse_version
    apps = App.objects.all()
    _version = parse_version(get_current_version())._version
    release = _version.release
    version = [str(x) for x in release]
    context = {
        'apps': apps,
        'site_apps': get_apps_names(),
        'version_info': {
            'current_version': ".".join(version),
            'backward_versions': get_backward_compatible()
        }
    }
    return render(request, 'app_manager/manage.html', context)


def home(request):
    return render(request, 'app_manager/rest_api/home.html', )


def index(request):
    Apps = installed_apps()
    context = {'Apps': Apps}
    return render(request, 'app_manager/apps.html', context)


@staff_member_required
@require_POST
@transaction.atomic
def install_app(request, store_id, app_name, version):
    response_data = {'success': False, 'messages': []}
    # TODO: remove try
    try:
        installer = AppInstaller(app_name, store_id, version, request.user)
        installer.install()
        response_data["success"] = True
    except Exception as ex:
        logger.error(ex)
        response_data["messages"].append({"type": "error", "msg": ex})

    return HttpResponse(
        json.dumps(response_data), content_type="application/json")


@staff_member_required
@require_POST
def uninstall_app(request, store_id, app_name):
    response_data = {"success": False, "errors": []}
    try:
        installer = AppInstaller(app_name, store_id, user=request.user)
        installer.uninstall(restart=False)
        response_data["success"] = True
    except Exception as ex:
        logger.error(ex)
        response_data["errors"].append(ex)
    return HttpResponse(
        json.dumps(response_data), content_type="application/json")


@login_required
def move_up(request, app_id):
    app = App.objects.get(id=app_id)
    prev_app = App.objects.get(
        order=App.objects.filter(
            order__lt=app.order).aggregate(Max('order'))['order__max'])
    order = app.order
    app.order = prev_app.order
    prev_app.order = order
    app.save()
    prev_app.save()
    return HttpResponse(
        json.dumps({
            "success": True
        }), content_type="application/json")


@login_required
def move_down(request, app_id):
    app = App.objects.get(id=app_id)
    next_app = App.objects.get(
        order=App.objects.filter(
            order__gt=app.order).aggregate(Min('order'))['order__min'])
    order = app.order
    app.order = next_app.order
    next_app.order = order
    app.save()
    next_app.save()
    return HttpResponse(
        json.dumps({
            "success": True
        }), content_type="application/json")


def save_app_orders(request):
    if request.method == 'POST':
        apps_list = request.POST.get('apps', None)

        if apps_list:
            try:
                apps = json.loads(apps_list)
                menu_apps = apps['menu_apps']
                non_menu_apps = apps['non_menu_apps']
                for idx, val in enumerate(menu_apps):
                    app = App.objects.get(id=int(val['id']))
                    app.order = idx
                    app.in_menu = True
                    app.save()

                for idx, val in enumerate(non_menu_apps):
                    app = App.objects.get(id=int(val['id']))
                    app.order = idx + len(menu_apps)
                    app.in_menu = False
                    app.save()
                ajax_vars = {'success': True}
            except BaseException:
                ajax_vars = {'success': False}
                return HttpResponse(
                    json.dumps(ajax_vars), content_type="application/json")

    return HttpResponse(json.dumps(ajax_vars), content_type="application/json")


def appinstance_detail(request, appinstanceid):
    """
    The view that show details of each document
    """
    appinstance = None
    try:
        appinstance = resolve_appinstance(request, appinstanceid,
                                          'base.view_resourcebase',
                                          PERMISSION_MSG_VIEW)

    except Http404:
        return render(request, '404.html', context={}, status=404)

    except PermissionDenied:
        return render(request, '401.html', context={
            'error_message':
                _("You are not allowed to view this document.")
        }, status=403)

    if appinstance is None:
        return HttpResponse(
            'An unknown error has occured.', mimetype="text/plain", status=401)

    else:
        if request.user != appinstance.owner and not request.user.is_superuser:
            AppInstance.objects.filter(id=appinstance.id).update(
                popular_count=F('popular_count') + 1)
        set_thumbnail_link = appinstance.link_set.filter(
            link_type='appinstance_thumbnail')
        context_dict = {
            'perms_list':
                get_perms(request.user, appinstance.get_self_resource()),
            'permissions_json':
                _perms_info_json(appinstance),
            'resource':
                appinstance,
            # 'appinstance_links': appinstance_links,
            'set_thumbnail_link':
                set_thumbnail_link
            # 'imgtypes': IMGTYPES,
            # 'related': related
        }

        if settings.SOCIAL_ORIGINS:
            context_dict["social_links"] = build_social_links(
                request, appinstance)

        if getattr(settings, 'EXIF_ENABLED', False):
            try:
                from geonode.contrib.exif.utils import exif_extract_dict
                exif = exif_extract_dict(appinstance)
                if exif:
                    context_dict['exif_data'] = exif
            except BaseException as e:
                logger.error(e.args[0] + "Exif extraction failed.")
        return render(request, "app_manager/appinstance_detail.html",
                      context=context_dict)
