# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib
import os
import sys
import threading

from future import standard_library

from cartoview.log_handler import get_logger

logger = get_logger(__name__, with_formatter=True)
lock = threading.Lock()
standard_library.install_aliases()

# BASE_DIR must be defined in project.settings

CARTOVIEW_APPS = ()
APPS_SETTINGS = []


def load_apps(APPS_DIR):
    with lock:
        from cartoview.apps_handler.utils import create_apps_dir
        from cartoview.apps_handler.config import CartoviewApp
        global CARTOVIEW_APPS
        global APPS_SETTINGS
        create_apps_dir(APPS_DIR)
        if APPS_DIR not in sys.path:
            sys.path.append(APPS_DIR)
        logger.info("Loading Cartoview Apps.....")
        CartoviewApp.apps_dir = APPS_DIR
        CartoviewApp.load()
        for app in CartoviewApp.objects.values():
            try:
                logger.info("Check if {} Healthy.\n".format(app.name))
                # ensure that the folder is python module
                app_module = importlib.import_module(app.name)
                app_dir = os.path.dirname(app_module.__file__)
                app_settings_file = os.path.join(app_dir, 'settings.py')
                libs_dir = os.path.join(app_dir, 'libs')
                if os.path.exists(app_settings_file):
                    # By doing this instead of import, app/settings.py can
                    # refer to local variables from settings.py without
                    # circular imports.
                    app_settings_file = os.path.realpath(app_settings_file)
                    APPS_SETTINGS += (app_settings_file,)
                if os.path.exists(libs_dir) and libs_dir not in sys.path:
                    logger.info(
                        "Append {} libs folder to the system path.\n".format(
                            app.name))
                    sys.path.append(libs_dir)
                logger.info("add {} to django INSTALLED_APPS.\n".format(app.name))
                if app.name not in CARTOVIEW_APPS:
                    # app_config.name.__str__() because Django don't like
                    # unicode_literals
                    CARTOVIEW_APPS += (app.name.__str__(),)
            except Exception as e:
                print(e)
                logger.error(e)
