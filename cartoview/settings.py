# -*- coding: utf-8 -*-
from __future__ import print_function

import ast
import copy
import os
import re
import sys

import dj_database_url
from distutils.util import strtobool
from geonode.settings import *  # noqa
from kombu import Exchange, Queue

import cartoview

PROJECT_NAME = "cartoview"

CARTOVIEW_INSTALLED_APPS = ("cartoview",
                            "cartoview.cartoview_api.apps.CartoviewAPIConfig",
                            "cartoview.store_api.apps.StoreApiConfig",
                            "cartoview.app_manager",
                            "cartoview.apps_handler.apps.AppsHandlerConfig")
INSTALLED_APPS += CARTOVIEW_INSTALLED_APPS

GEONODE_APPS_NAV_MENU_ENABLE = ast.literal_eval(os.getenv("GEONODE_APPS_NAV_MENU_ENABLE", "False"))

ROOT_URLCONF = os.getenv('ROOT_URLCONF', "cartoview.urls")
CARTOVIEW_DIR = os.path.abspath(os.path.dirname(cartoview.__file__))
BASE_DIR = os.path.dirname(CARTOVIEW_DIR)

CARTOVIEW_TEMPLATE_DIRS = [
    os.path.join(CARTOVIEW_DIR, "templates")
]
TEMPLATES[0]["DIRS"] = CARTOVIEW_TEMPLATE_DIRS + TEMPLATES[0]["DIRS"]

CARTOVIEW_STATIC_DIRS = [
    os.path.join(CARTOVIEW_DIR, "static"),
]
STATICFILES_DIRS = CARTOVIEW_STATIC_DIRS + STATICFILES_DIRS

APPS_DIR = os.getenv('APPS_DIR', os.path.abspath(os.path.join(os.path.dirname(CARTOVIEW_DIR), "apps")))
PENDING_APPS = os.path.join(APPS_DIR, "pendingOperation.yml")
APPS_MENU = False
DOCKER = os.getenv('DOCKER', False)
CARTOVIEW_CONTEXT_PROCESSORS = ('cartoview.app_manager.context_processors.cartoview_processor',)
TEMPLATES[0]["OPTIONS"]['context_processors'] += CARTOVIEW_CONTEXT_PROCESSORS
# django Media Section
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR, MEDIAFILES_LOCATION))

# static section
STATIC_ROOT = os.getenv('STATIC_ROOT', os.path.join(BASE_DIR, STATICFILES_LOCATION))

DATABASE_URL = os.getenv(
    'DATABASE_URL', 'spatialite:////{}/database.db'.format(
        os.path.dirname(CARTOVIEW_DIR)))
DATASTORE_DATABASE_URL = os.getenv('DATASTORE_DATABASE_URL', None)
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(
        DATABASE_URL, conn_max_age=0)
if DATASTORE_DATABASE_URL:
    DATABASES['datastore'] = dj_database_url.parse(
        DATASTORE_DATABASE_URL, conn_max_age=0)


CARTOVIEW_TEST = 'test' in sys.argv or ast.literal_eval(
    os.getenv('CARTOVIEW_TEST', "False")) or 'run_cartoview_test' in sys.argv

if CARTOVIEW_TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.spatialite',
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
        print(e)


# Location of translation files
_DEFAULT_LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

LOCALE_PATHS = os.getenv('LOCALE_PATHS', _DEFAULT_LOCALE_PATHS)


try:
    from .local_settings import *  # noqa
except Exception as e:
    print(e)
