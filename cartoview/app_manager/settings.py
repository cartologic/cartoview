import os
import sys
import importlib
from cartoview.app_manager.config import AppsConfig
# BASE_DIR must be defined in project.settings
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, "apps"))
if not os.path.exists(APPS_DIR):
    os.makedirs(APPS_DIR)
if APPS_DIR not in sys.path:
    sys.path.append(APPS_DIR)


apps_file_path =  os.path.join(APPS_DIR, "apps.yml")
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
        except:
            # TODO: log the error
            pass

INSTALLED_APPS = INSTALLED_APPS + CARTOVIEW_APPS
