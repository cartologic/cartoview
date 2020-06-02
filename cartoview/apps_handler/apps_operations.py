# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from future import standard_library

from cartoview.log_handler import get_logger

standard_library.install_aliases()
logger = get_logger(__name__)


class AppsHandler(object):
    def __init__(self):
        pass

    def delete_application_on_fail(self, appname):
        from cartoview.app_manager.installer import AppInstaller
        AppInstaller(appname).uninstall(restart=True)

    def get_pending_apps(self, app_name):
        app = {"name": app_name, "makemigrations": False, "migrate": True}
        DEFAULT_APPS = [
            app,
        ]
        apps = DEFAULT_APPS
        apps_dir = getattr(settings, 'APPS_DIR', None)
        _app_dir = os.path.join(apps_dir, app_name)
        app_data_file = os.path.join(_app_dir, 'installer.json')
        if os.path.exists(app_data_file) and os.access(app_data_file, os.R_OK):
            with open(app_data_file, 'r') as f:
                app_data = json.load(f)
                apps = app_data.get('apps', DEFAULT_APPS)
        return apps

    def makemigrations(self, app_name):
        call_command("makemigrations", app_name, interactive=False)

    def migrate(self, app_name):
        try:
            call_command("migrate", app_name, interactive=False)
        except CommandError as e:
            logger.error(e)
            if e.args[0] and "does not have migrations" not in e.args[0]:
                self.delete_application_on_fail(app_name)

    def collectstatic(self):
        if not settings.DEBUG:
            call_command(
                "collectstatic",
                interactive=False,
                ignore=['node_modules', '.git'])

    def execute_pending(self):
        from cartoview.apps_handler.config import CartoviewApp
        CartoviewApp.load()
        pending_apps = CartoviewApp.objects.get_pending_apps().values()
        for app in pending_apps:
            _pending_apps = self.get_pending_apps(app.name)
            if _pending_apps:
                for _app in _pending_apps:
                    _app_name = _app.get('name', None)
                    _make_migrations = _app.get('makemigrations', False)
                    _migrate = _app.get('migrate', False)
                    if _app_name:
                        if _make_migrations:
                            self.makemigrations(_app_name)
                        if _migrate:
                            self.migrate(_app_name)
            else:
                self.migrate(app)
            self.collectstatic()
            carto_app = CartoviewApp.objects.get(app.name)
            carto_app.pending = False
            carto_app.commit()
            CartoviewApp.save()

    def __call__(self):
        apps_dir = getattr(settings, 'APPS_DIR', None)
        if apps_dir and os.path.exists(apps_dir):
            self.execute_pending()


pending_handler = AppsHandler()
