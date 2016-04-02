# -*- coding: utf-8 -*-
print PROJECT_ROOT
import os
execfile(os.path.join(PROJECT_ROOT, 'pre_settings.py'))
import geonode
GEONODE_ROOT = os.path.abspath(os.path.dirname(geonode.__file__))

execfile(os.path.join(GEONODE_ROOT, 'settings.py'))
import cartoview
CARTOVIEW_ROOT = LOCAL_ROOT = os.path.abspath(os.path.dirname(cartoview.__file__))

# Defines settings for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'cartoview.sqlite'),
    }
}

site_name = os.path.basename(PROJECT_ROOT)
WSGI_APPLICATION = "cartoview.wsgi.application"

# override Geonode media and static root
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.path.pardir, "uploaded"))
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.path.pardir, "static"))
MEDIA_URL = '/uploaded/'


# Additional directories which hold static files
STATICFILES_DIRS.append(os.path.join(PROJECT_ROOT, "static"))
STATICFILES_DIRS.append(os.path.join(GEONODE_ROOT, "static"))
print os.path.join(GEONODE_ROOT, "static")
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),
                 os.path.join(CARTOVIEW_ROOT, "templates"),
                 os.path.join(GEONODE_ROOT, "templates"),
                ) + TEMPLATE_DIRS

# Location of url mappings
ROOT_URLCONF = 'cartoview.urls'
print CARTOVIEW_ROOT
# Location of locale files
LOCALE_PATHS = (
   os.path.join(CARTOVIEW_ROOT, 'locale'),
   os.path.join(PROJECT_ROOT, 'locale'),
) + LOCALE_PATHS


CARTOVIEW_APPS = (
    'bootstrap3',
    'cartoview',
    'cartoview.app_manager',
    'cartoview.basic.geonode_map_application',

)


import sys, importlib
APPS_DIR = os.path.join(PROJECT_ROOT, os.pardir, "apps")
sys.path.append(APPS_DIR)
apps_names = [n for n in os.listdir(APPS_DIR) if os.path.isdir(os.path.join(APPS_DIR, n))]

for app_name in apps_names:
    print app_name
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

INSTALLED_APPS = CARTOVIEW_APPS + INSTALLED_APPS

SITEURL = 'http://localhost:8000/'
DEFAULT_WORKSPACE = "cartoview"
GEOSERVER_URL = 'http://localhost:8080/geoserver/'
GEOSERVER_PUBLIC_URL = 'http://localhost:8080/geoserver/'
IS_ADMIN_SITE = True

execfile(os.path.join(PROJECT_ROOT, 'local_settings.py'))

OGC_SERVER['default']['LOCATION'] = GEOSERVER_URL
#OGC_SERVER['default']['LOCATION'] = os.path.join(SITEURL, 'geoserver/')
OGC_SERVER['default']['PUBLIC_LOCATION'] = GEOSERVER_PUBLIC_URL
try:
    OGC_SERVER['default']['DATASTORE'] = GEOSERVER_DATASTORE
except:
    pass


try:
    MAP_BASELAYERS.remove(LOCAL_GEOSERVER)
    # LOCAL_GEOSERVER ["source"]["url"] = OGC_SERVER['default']['PUBLIC_LOCATION'] + DEFAULT_WORKSPACE + "/wms"
    LOCAL_GEOSERVER ["source"]["url"] = OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms"
    baselayers = MAP_BASELAYERS
    MAP_BASELAYERS = [LOCAL_GEOSERVER]
    MAP_BASELAYERS.extend(baselayers)
except:
    pass