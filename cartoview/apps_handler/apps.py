# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.conf import settings
import yaml
import os
import logging
from sys import stdout
from django.core.management import call_command
from django.core.management.base import CommandError
pending_yaml = settings.PENDING_APPS
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

    def reset(self):
        with open(pending_yaml, 'w+') as f:
            yaml.dump([], f)

    def execute_pending(self):
        # TODO: fix racing
        if os.path.exists(pending_yaml):
            with open(pending_yaml, 'r') as f:
                pending_apps = yaml.load(f) or []
                for app in pending_apps:
                    try:
                        call_command("collectstatic", interactive=False,
                                     ignore=['node_modules'])
                        call_command("makemigrations", app,
                                     interactive=False)
                        call_command("migrate", app,
                                     interactive=False)
                    except CommandError as e:
                        error = e.message
                        logger.error(error)
                        if "you cannot selectively sync unmigrated apps"\
                                not in error:
                            self.delete_application_on_fail(app)
            self.reset()
        else:
            pass

    def ready(self):
        self.execute_pending()
