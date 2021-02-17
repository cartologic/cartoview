# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Max, Min
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from future import standard_library

from cartoview.log_handler import get_logger
from .installer import AppInstaller
from .models import App

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
