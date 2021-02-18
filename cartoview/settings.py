# -*- coding: utf-8 -*-
from __future__ import print_function

import ast
import copy
import os
import re
import sys
from distutils.util import strtobool

import dj_database_url
from geonode.settings import *  # noqa
from kombu import Exchange, Queue

import cartoview

CARTOVIEW_DIR = os.path.abspath(os.path.dirname(cartoview.__file__))
BASE_DIR = os.path.dirname(CARTOVIEW_DIR)
APPS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(CARTOVIEW_DIR), "apps"))
PENDING_APPS = os.path.join(APPS_DIR, "pendingOperation.yml")

try:
    # try to parse python notation, default in dockerized env
    ALLOWED_HOSTS = ast.literal_eval(os.getenv('ALLOWED_HOSTS'))
except ValueError:
    # fallback to regular list of values separated with misc chars
    ALLOWED_HOSTS = ['*'] if os.getenv('ALLOWED_HOSTS') is None \
        else re.split(r' *[,|:|;] *', os.getenv('ALLOWED_HOSTS'))

DOCKER = os.getenv('DOCKER', False)

PROJECT_NAME = "cartoview"

SITE_NAME = "CartoView"

SITEURL = os.getenv('SITEURL', "http://localhost/")

ROOT_URLCONF = os.getenv('ROOT_URLCONF', "cartoview.urls")

DATABASE_URL = os.getenv(
    'DATABASE_URL', 'sqlite:////{}/database.sqlite'.format(
        os.path.dirname(CARTOVIEW_DIR)))
DATASTORE_DATABASE_URL = os.getenv('DATASTORE_DATABASE_URL', None)
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(
        DATABASE_URL, conn_max_age=0)
if DATASTORE_DATABASE_URL:
    DATABASES['datastore'] = dj_database_url.parse(
        DATASTORE_DATABASE_URL, conn_max_age=0)

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded")
MEDIA_URL = "/uploaded/"
LOCAL_MEDIA_URL = "/uploaded/"

# ---
# Override GeoNode Settings
# ---
if 'datastore' in DATABASES:
    OGC_SERVER['default']['DATASTORE'] = 'datastore'
if 'geonode.geoserver' in INSTALLED_APPS and "LOCAL_GEOSERVER" in \
        locals() and LOCAL_GEOSERVER in MAP_BASELAYERS:
    LOCAL_GEOSERVER["source"][
        "url"] = OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms"
# default uploader.
os.environ.setdefault('DEFAULT_BACKEND_UPLOADER', 'geonode.importer')

# ---
# CartoView Settings
# ---
CARTOVIEW_INSTALLED_APPS = (
    "cartoview",
    "cartoview.app_manager.apps.AppsHandlerConfig",
    "cartoview.site_management",
)
INSTALLED_APPS += CARTOVIEW_INSTALLED_APPS

CARTOVIEW_TEMPLATE_DIRS = [
    os.path.join(CARTOVIEW_DIR, "templates"),
]
TEMPLATES[0]["DIRS"] = CARTOVIEW_TEMPLATE_DIRS

CARTOVIEW_STATIC_DIRS = [
    os.path.join(CARTOVIEW_DIR, "static"),
]
STATICFILES_DIRS += CARTOVIEW_STATIC_DIRS

APPS_MENU = False

CARTOVIEW_CONTEXT_PROCESSORS = (
    'cartoview.app_manager.context_processors.cartoview_processor',
    'cartoview.app_manager.context_processors.site_logo'
)
TEMPLATES[0]["OPTIONS"]['context_processors'] += CARTOVIEW_CONTEXT_PROCESSORS

CARTOVIEW_TEST = 'test' in sys.argv or ast.literal_eval(
    os.getenv('CARTOVIEW_TEST', "False")) or 'run_cartoview_test' in sys.argv

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

# if cartoview without cartoview_project_template
CARTOVIEW_STAND_ALONE = strtobool(os.getenv('CARTOVIEW_STAND_ALONE', 'TRUE'))

CARTOVIEW_TEST = 'test' in sys.argv or ast.literal_eval(
    os.getenv('CARTOVIEW_TEST', "False")) or 'run_cartoview_test' in sys.argv

if CARTOVIEW_TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'test.db')
        }
    }

if CARTOVIEW_STAND_ALONE or CARTOVIEW_TEST:
    try:
        from .cartoview_apps_settings import *
    except Exception as e:
        print(f'Error while importing cartoview_apps_settings : {e}')

# Import local_settings to override any of the above settings
try:
    from .local_settings import *  # noqa
except Exception as e:
    print(f'Error while importing local_settings: {e}')
