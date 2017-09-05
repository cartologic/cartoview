from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from past.builtins import execfile
import importlib
import logging
import os
import sys
from sys import stdout

from cartoview.app_manager.config import AppsConfig

formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s  { %(name)s %(pathname)s:%(lineno)d} \
                            %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
# BASE_DIR must be defined in project.settings
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, "apps"))
if not os.path.exists(APPS_DIR):
    os.makedirs(APPS_DIR)
if APPS_DIR not in sys.path:
    sys.path.append(APPS_DIR)

apps_file_path = os.path.join(APPS_DIR, "apps.yml")
apps_config = AppsConfig(apps_file_path)
CARTOVIEW_APPS = ()
for app_config in apps_config:
    if app_config.active:
        try:
            # ensure that the folder is python module
            app_module = importlib.import_module(app_config.name)
            app_dir = os.path.dirname(app_module.__file__)
            app_settings_file = os.path.join(app_dir, 'settings.py')
            if os.path.exists(app_settings_file):
                # By doing this instead of import, app/settings.py can refer to
                # local variables from settings.py without circular imports.
                execfile(app_settings_file)
            if app_config.name not in CARTOVIEW_APPS:
                CARTOVIEW_APPS += (app_config.name,)
        except Exception as e:
            logger.error(e.message)

INSTALLED_APPS = INSTALLED_APPS + CARTOVIEW_APPS
