# -*- coding: utf-8 -*-

from django.apps import AppConfig
import logging
from sys import stdout
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s  { %(name)s %(pathname)s:%(lineno)d} \
                            %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


class AppsManagerConfig(AppConfig):
    name = 'cartoview.app_manager'
    verbose_name = "App Manager"

    def ready(self):
        pass
