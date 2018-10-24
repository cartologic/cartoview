# -*- coding: utf-8 -*-
import ast
import os
import re
import copy
import sys
from distutils.util import strtobool

import dj_database_url
from geonode.settings import *

import cartoview

CARTOVIEW_INSTALLED_APPS = ("cartoview",
                            "cartoview.cartoview_api.apps.CartoviewAPIConfig",
                            "cartoview.app_manager",
                            "cartoview.site_management",
                            "cartoview.apps_handler.apps.AppsHandlerConfig")
INSTALLED_APPS += CARTOVIEW_INSTALLED_APPS
ROOT_URLCONF = "cartoview.urls"
CARTOVIEW_DIR = os.path.abspath(os.path.dirname(cartoview.__file__))
BASE_DIR = os.path.dirname(CARTOVIEW_DIR)
CARTOVIEW_TEMPLATE_DIRS = [
    os.path.join(CARTOVIEW_DIR, "templates"),
]
# TEMPLATES[0]["DIRS"] = CARTOVIEW_TEMPLATE_DIRS
CARTOVIEW_STATIC_DIRS = [
    os.path.join(CARTOVIEW_DIR, "static"),
]
STATICFILES_DIRS += CARTOVIEW_STATIC_DIRS
APPS_DIR = os.path.abspath(os.path.join(
    os.path.dirname(CARTOVIEW_DIR), "apps"))
PENDING_APPS = os.path.join(APPS_DIR, "pendingOperation.yml")
APPS_MENU = False
DOCKER = os.getenv('DOCKER', False)
CARTOVIEW_CONTEXT_PROCESSORS = (
    'cartoview.app_manager.context_processors.cartoview_processor',
    'cartoview.app_manager.context_processors.site_logo')
TEMPLATES[0]["OPTIONS"]['context_processors'] += CARTOVIEW_CONTEXT_PROCESSORS
# django Media Section
# uncomment the following if you want your files out of geonode folder
MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded")
MEDIA_URL = "/uploaded/"
LOCAL_MEDIA_URL = "/uploaded/"
# static section
STATIC_ROOT = os.path.join(BASE_DIR, "static")
DATABASE_URL = os.getenv(
    'DATABASE_URL', 'sqlite:////{}/database.sqlite'.format(
    os.path.dirname(CARTOVIEW_DIR)))
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

CARTOVIEW_TEST = 'test' in sys.argv or ast.literal_eval(
    os.getenv('CARTOVIEW_TEST', "False")) or 'run_cartoview_test' in sys.argv

if CARTOVIEW_TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'test.db')
        }
    }
if 'datastore' in DATABASES:
    OGC_SERVER['default']['DATASTORE'] = 'datastore'

if 'geonode.geoserver' in INSTALLED_APPS and "LOCAL_GEOSERVER" in \
        locals() and LOCAL_GEOSERVER in MAP_BASELAYERS:
    LOCAL_GEOSERVER["source"][
        "url"] = OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms"

# Logging settings
# 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'
DJANGO_LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'ERROR')

installed_apps_conf = {
    'handlers': ['console'],
    'level': DJANGO_LOG_LEVEL,
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            ('%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d'
             ' %(message)s'),
        },
    },
    'handlers': {
        'console': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers':
    {app: copy.deepcopy(installed_apps_conf)
     for app in INSTALLED_APPS},
    'root': {
        'handlers': ['console'],
        'level': DJANGO_LOG_LEVEL
    },
}

LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['console'],
    'propagate': False,
    'level': 'WARNING',  # Django SQL logging is too noisy at DEBUG
}

# NOTE:set cartoview_stand_alone environment var if you are not using
# cartoview_proect_template
CARTOVIEW_STAND_ALONE = strtobool(os.getenv('CARTOVIEW_STAND_ALONE', 'FALSE'))
if CARTOVIEW_STAND_ALONE or CARTOVIEW_TEST:
    TEMPLATES[0]["DIRS"] = CARTOVIEW_TEMPLATE_DIRS + TEMPLATES[0]["DIRS"]
    from cartoview import app_manager
    from past.builtins import execfile
    app_manager_settings = os.path.join(
        os.path.dirname(app_manager.__file__), "settings.py")
    execfile(os.path.realpath(app_manager_settings))
    load_apps(APPS_DIR)
    INSTALLED_APPS += CARTOVIEW_APPS
    for settings_file in APPS_SETTINGS:
        try:
            execfile(settings_file)
        except Exception as e:
            print(e.message)
