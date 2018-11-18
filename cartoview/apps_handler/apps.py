# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from django.apps import AppConfig
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from future import standard_library

from cartoview.log_handler import get_logger

standard_library.install_aliases()
pending_yaml = settings.PENDING_APPS

logger = get_logger(__name__)


class AppsHandlerConfig(AppConfig):
    name = 'cartoview.apps_handler'
    verbose_name = "Apps Handler"

    def delete_application_on_fail(self, appname):
        from cartoview.app_manager.installer import AppInstaller
        AppInstaller(appname).uninstall(restart=True)

    def execute_pending(self):
        from cartoview.apps_handler.handlers import CartoApps, apps_orm
        with apps_orm.session() as session:
            pending_apps = session.query(CartoApps).filter(
                CartoApps.pending == True).all()  # noqa
            for app in pending_apps:
                try:
                    if not settings.DEBUG:
                        call_command(
                            "collectstatic",
                            interactive=False,
                            ignore=['node_modules', '.git'])
                    call_command("migrate", app.name, interactive=False)
                except CommandError as e:
                    error = e.message
                    logger.error(error)
                    if error and "does not have migrations" not in error:
                        self.delete_application_on_fail(app.name)
                finally:
                    CartoApps.set_app_pending(app.name, False)

    def ready(self):
        apps_dir = getattr(settings, 'APPS_DIR', None)
        if apps_dir and os.path.exists(apps_dir):
            self.execute_pending()
