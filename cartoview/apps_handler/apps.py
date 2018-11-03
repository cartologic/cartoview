# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from cartoview.log_handler import get_logger
from cartoview.apps_handler.handlers import CartoApps, apps_orm
pending_yaml = settings.PENDING_APPS

logger = get_logger(__name__)


class AppsHandlerConfig(AppConfig):
    name = 'cartoview.apps_handler'
    verbose_name = "Apps Handler"

    def delete_application_on_fail(self, appname):
        from cartoview.app_manager.installer import AppInstaller
        AppInstaller(appname).uninstall(restart=True)

    def execute_pending(self):
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
                    if "you cannot selectively sync unmigrated apps"\
                            not in error:
                        self.delete_application_on_fail(app.name)

    def ready(self):
        self.execute_pending()
