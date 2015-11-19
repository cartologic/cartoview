from settings import *

CARTOVIEW_ROOT = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'cartoview')
STATICFILES_DIRS.extend([os.path.join(CARTOVIEW_ROOT, "static")])

# Add cartoview.app_manager to INSTALLED_APPS before GEONODE_APPS
INSTALLED_APPS = tuple(i for i in INSTALLED_APPS if i not in GEONODE_APPS)
INSTALLED_APPS += ('cartoview.app_manager',)
INSTALLED_APPS += GEONODE_APPS

if 'cartoview.app_manager' in INSTALLED_APPS:
    # auto load apps
    from cartoview.app_manager.apps_helper import get_apps_names, APPS_DIR

    CARTOVIEW_APPS = ()

    import importlib, sys

    for app_name in get_apps_names():
        try:
            CARTOVIEW_APPS += ('cartoview.apps.' + app_name,)
            # settings_module = importlib.import_module('apps.%s.settings' % app_name)
            app_settings_file = os.path.join(APPS_DIR, app_name, 'settings.py')
            if os.path.exists(app_settings_file):
                # By doing this instead of import, app/settings.py can refer to
                # local variables from settings.py without circular imports.
                execfile(app_settings_file)
        except:
            pass

    INSTALLED_APPS += CARTOVIEW_APPS

# Uncomment this line incase a restart server batch exists.
# RESTART_SERVER_BAT = "D:/geonode_devolopment/geonode-master/restart_server.bat"
