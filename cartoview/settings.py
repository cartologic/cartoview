from geonode.settings import *
INSTALLED_APPS += ("cartoview", "cartoview.app_manager", "cartoview.user_engage", )
ROOT_URLCONF = "cartoview.urls"
import geonode
import cartoview
CARTOVIEW_ROOT = os.path.abspath(os.path.dirname(cartoview.__file__))
GEONODE_ROOT = os.path.abspath(os.path.dirname(geonode.__file__))
TEMPLATES[0]["DIRS"] = [os.path.join(CARTOVIEW_ROOT, "templates")] + TEMPLATES[0]["DIRS"]
STATICFILES_DIRS += [os.path.join(CARTOVIEW_ROOT, "static"),]
cartoview_apps_settings_path = os.path.join(CARTOVIEW_ROOT, 'app_manager', "settings.py")
TEMPLATES[0]["OPTIONS"]['context_processors'] += ('cartoview.app_manager.context_processors.apps','cartoview.app_manager.context_processors.news')
execfile(cartoview_apps_settings_path)
