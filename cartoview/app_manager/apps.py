# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

from django.apps import AppConfig
from future import standard_library

from cartoview.log_handler import get_logger
from .apps_operations import pending_handler

standard_library.install_aliases()

logger = get_logger(__name__)


class AppManagerConfig(AppConfig):
    name = 'cartoview.app_manager'
    verbose_name = "CartoView App Manager"

    def ready(self):
        pending_handler()
