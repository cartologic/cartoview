# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.apps import AppConfig
from future import standard_library

from cartoview.apps_handler.apps_operations import pending_handler
from cartoview.log_handler import get_logger

standard_library.install_aliases()

logger = get_logger(__name__)


class AppsHandlerConfig(AppConfig):
    name = 'cartoview.apps_handler'
    verbose_name = "Apps Handler"

    def ready(self):
        pending_handler()
