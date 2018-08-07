# -*- coding: utf-8 -*-
import os
from distutils.util import strtobool

from geonode.settings import *
import ast
import re
import dj_database_url
import cartoview
import sys
INSTALLED_APPS += ("cartoview",
                   "cartoview.cartoview_api.apps.CartoviewAPIConfig",
                   "cartoview.app_manager", "cartoview.site_management",
                   "cartoview.apps_handler.apps.AppsHandlerConfig")
ROOT_URLCONF = "cartoview.urls"
CARTOVIEW_DIR = os.path.abspath(os.path.dirname(cartoview.__file__))
BASE_DIR = os.path.dirname(CARTOVIEW_DIR)
CARTOVIEW_TEMPLATE_DIRS = [os.path.join(CARTOVIEW_DIR, "templates")
                           ] + TEMPLATES[0]["DIRS"]
# TEMPLATES[0]["DIRS"] = CARTOVIEW_TEMPLATE_DIRS
CARTOVIEW_STATIC_DIRS = [
    os.path.join(CARTOVIEW_DIR, "static"),
]
STATICFILES_DIRS += CARTOVIEW_STATIC_DIRS
APPS_DIR = os.path.abspath(os.path.join(CARTOVIEW_DIR, "apps"))
PENDING_APPS = os.path.join(APPS_DIR, "pendingOperation.yml")
APPS_MENU = False
DOCKER = os.getenv('DOCKER', False)
CARTOVIEW_CONTEXT_PROCESSORS = (
    'cartoview.app_manager.context_processors.cartoview_processor',
    'cartoview.app_manager.context_processors.site_logo'
)
TEMPLATES[0]["OPTIONS"]['context_processors'] += CARTOVIEW_CONTEXT_PROCESSORS
# bower static files
STATICFILES_DIRS += [
    os.path.join(CARTOVIEW_DIR, "static"),
]
# django Media Section
# uncomment the following if you want your files out of geonode folder
MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded")
MEDIA_URL = "/uploaded/"
LOCAL_MEDIA_URL = "/uploaded/"
# static section
STATIC_ROOT = os.path.join(BASE_DIR, "static")
DATABASE_URL = os.getenv('DATABASE_URL', None)
DATASTORE_DATABASE_URL = os.getenv('DATASTORE_DATABASE_URL', None)
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(
        DATABASE_URL, conn_max_age=600)
if DATASTORE_DATABASE_URL:
    DATABASES['datastore'] = dj_database_url.parse(
        DATASTORE_DATABASE_URL, conn_max_age=600)
try:
    # try to parse python notation, default in dockerized env
    ALLOWED_HOSTS = ast.literal_eval(os.getenv('ALLOWED_HOSTS'))
except ValueError:
    # fallback to regular list of values separated with misc chars
    ALLOWED_HOSTS = ['*'] if os.getenv('ALLOWED_HOSTS') is None \
        else re.split(r' *[,|:|;] *', os.getenv('ALLOWED_HOSTS'))
try:
    from .local_settings import *
except Exception as e:
    pass
if 'test' in sys.argv:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', }}
if 'datastore' in DATABASES:
    OGC_SERVER['default']['DATASTORE'] = 'datastore'

if 'geonode.geoserver' in INSTALLED_APPS and "LOCAL_GEOSERVER" in \
        locals() and LOCAL_GEOSERVER in MAP_BASELAYERS:
    LOCAL_GEOSERVER["source"][
        "url"] = OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms"

# NOTE:set cartoview_stand_alone environment var if you are not using cartoview_proect_template
CARTOVIEW_STAND_ALONE = strtobool(os.getenv('CARTOVIEW_STAND_ALONE', 'FALSE'))
if CARTOVIEW_STAND_ALONE:
    TEMPLATES[0]["DIRS"] = CARTOVIEW_TEMPLATE_DIRS
    from cartoview.app_manager.settings import load_apps
    INSTALLED_APPS += load_apps()
