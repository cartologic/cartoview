# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib
import os
import sys

from future import standard_library
from past.builtins import execfile

from cartoview.app_manager.config import AppsConfig
from cartoview.app_manager.helpers import (change_path_permission,
                                           create_direcotry)
from cartoview.log_handler import get_logger

logger = get_logger(__name__)

standard_library.install_aliases()

# BASE_DIR must be defined in project.settings

CARTOVIEW_APPS = ()
APPS_SETTINGS = []


def create_apps_dir(APPS_DIR):
    if not os.path.exists(APPS_DIR):
        create_direcotry(APPS_DIR)
        if not os.access(APPS_DIR, os.W_OK):
            change_path_permission(APPS_DIR)


def load_apps(APPS_DIR):
    global CARTOVIEW_APPS
    global APPS_SETTINGS
    create_apps_dir(APPS_DIR)
    if APPS_DIR not in sys.path:
        sys.path.append(APPS_DIR)
    apps_file_path = os.path.join(APPS_DIR, "apps.yml")
    apps_config = AppsConfig(apps_file_path)
    for app_config in apps_config:
        if app_config.active:
            try:
                # ensure that the folder is python module
                app_module = importlib.import_module(app_config.name)
                app_dir = os.path.dirname(app_module.__file__)
                app_settings_file = os.path.join(app_dir, 'settings.py')
                libs_dir = os.path.join(app_dir, 'libs')
                if os.path.exists(app_settings_file):
                    # By doing this instead of import, app/settings.py can
                    # refer to local variables from settings.py without
                    # circular imports.
                    app_settings_file = os.path.realpath(app_settings_file)
                    APPS_SETTINGS += (app_settings_file,)
                    # execfile(app_settings_file)
                if os.path.exists(libs_dir) and libs_dir not in sys.path:
                    sys.path.append(libs_dir)
                if app_config.name not in CARTOVIEW_APPS:
                    # app_config.name.__str__() because Django don't like
                    # unicode_literals
                    CARTOVIEW_APPS += (app_config.name.__str__(), )
            except Exception as e:
                print(e.message)
                logger.error(e.message)
