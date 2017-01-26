import os
import sys
import importlib

# BASE_DIR must be defined in project.settings
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, "apps"))
if not os.path.exists(APPS_DIR):
    os.makedirs(APPS_DIR)

apps_names = [n for n in os.listdir(APPS_DIR) if os.path.isdir(os.path.join(APPS_DIR, n))]
sys.path.append(APPS_DIR)
CARTOVIEW_APPS = ()
for app_name in apps_names:
    # print app_name
    try:
        # ensure that the folder is python module
        app_module = importlib.import_module(app_name)
        app_dir = os.path.dirname(app_module.__file__)
        app_settings_file = os.path.join(app_dir, 'settings.py')
        if os.path.exists(app_settings_file):
            # By doing this instead of import, app/settings.py can refer to
            # local variables from settings.py without circular imports.
            execfile(app_settings_file)
        if app_name not in CARTOVIEW_APPS:
            CARTOVIEW_APPS += (app_name,)
    except:
        # TODO: log the error
        pass

INSTALLED_APPS = INSTALLED_APPS + CARTOVIEW_APPS
