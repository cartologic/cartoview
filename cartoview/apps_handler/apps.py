# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.conf import settings
import yaml
import os
import logging
from sys import stdout
from django.core.management import call_command
from django.core.management.base import CommandError
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s  { %(name)s %(pathname)s:%(lineno)d} \
                            %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


class AppsHandlerConfig(AppConfig):
    name = 'cartoview.apps_handler'
    verbose_name = "Apps Handler"

    def delete_application_on_fail(self, appname):
        from cartoview.app_manager.installer import AppInstaller
        AppInstaller(appname).uninstall(restart=True)

    def execute_pending(self):
        # TODO: fix racing
        pending_yaml = settings.PENDING_APPS
        if os.path.exists(pending_yaml):
            with open(pending_yaml, 'r') as f:
                pending_apps = yaml.load(f) or []
                for app in pending_apps:
                    call_command("makemigrations", app, interactive=False)
                    try:
                        call_command("migrate", app, interactive=False)
                    except CommandError:
                        self.delete_application_on_fail(app)
            with open(pending_yaml, 'w+') as f:
                yaml.dump([], f)
        else:
            pass

    def ready(self):
        self.execute_pending()
