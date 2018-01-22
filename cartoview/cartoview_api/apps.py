# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.conf import settings
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


class CartoviewAPIConfig(AppConfig):
    name = 'cartoview.cartoview_api'
    verbose_name = "Cartoview API"
