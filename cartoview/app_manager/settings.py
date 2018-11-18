# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib
import os
import sys

from future import standard_library
from past.builtins import execfile

from cartoview.apps_handler.handlers import CartoApps, apps_orm
from cartoview.apps_handler.utils import create_apps_dir
from cartoview.log_handler import get_logger

logger = get_logger(__name__, with_formatter=True)

standard_library.install_aliases()

# BASE_DIR must be defined in project.settings

CARTOVIEW_APPS = ()
APPS_SETTINGS = []


def load_apps(APPS_DIR):
    global CARTOVIEW_APPS
    global APPS_SETTINGS
    create_apps_dir(APPS_DIR)
    if APPS_DIR not in sys.path:
        sys.path.append(APPS_DIR)
    # apps_file_path = os.path.join(APPS_DIR, "apps.yml")
    # apps_config = AppsConfig(apps_file_path)
    logger.info("Loading Cartoview Apps.....")
    with apps_orm.session() as session:
        carto_apps = session.query(CartoApps).filter(
            CartoApps.active == True).all()
    for app in carto_apps:
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
                APPS_SETTINGS += (app_settings_file, )
                # execfile(app_settings_file)
            if os.path.exists(libs_dir) and libs_dir not in sys.path:
                logger.info("Install {} libs folder to the system.\n".format(
                    app.name))
                sys.path.append(libs_dir)
            logger.info("add {} to INSTALLED_APPS.\n".format(app.name))
            if app.name not in CARTOVIEW_APPS:
                # app_config.name.__str__() because Django don't like
                # unicode_literals
                CARTOVIEW_APPS += (app.name.__str__(), )
        except Exception as e:
            print(e.message)
            logger.error(e.message)
