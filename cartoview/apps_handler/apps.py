# -*- coding: utf-8 -*-

import os

import portalocker
import yaml
from django.apps import AppConfig
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from cartoview.log_handler import get_logger

pending_yaml = settings.PENDING_APPS

logger = get_logger(__name__)


class AppsHandlerConfig(AppConfig):
    name = 'cartoview.apps_handler'
    verbose_name = "Apps Handler"

    def delete_application_on_fail(self, appname):
        from cartoview.app_manager.installer import AppInstaller
        AppInstaller(appname).uninstall(restart=True)

    def reset(self):
        with open(pending_yaml, 'w+') as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            yaml.dump([], f)

    def execute_pending(self):
        if os.path.exists(pending_yaml):
            with open(pending_yaml, 'r') as f:
                pending_apps = yaml.load(f) or []
                for app in pending_apps:
                    try:
                        if not settings.DEBUG:
                            call_command(
                                "collectstatic",
                                interactive=False,
                                ignore=['node_modules', '.git'])
                        call_command("migrate", app, interactive=False)
                    except CommandError as e:
                        error = e.message
                        logger.error(error)
                        if "you cannot selectively sync unmigrated apps"\
                                not in error:
                            self.delete_application_on_fail(app)
            self.reset()

    def ready(self):
        self.execute_pending()
