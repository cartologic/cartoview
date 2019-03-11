# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppManagerConfig(AppConfig):
    name = 'cartoview.app_manager'
    verbose_name = _('App Manager')

    def ready(self):
        from .os_utils import create_apps_dir
        create_apps_dir()
        from .apps_operations import pending_handler
        pending_handler.execute_pending()
