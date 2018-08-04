# -*- coding: utf-8 -*-
import os
from distutils.util import strtobool

from geonode.settings import *
import ast
import re
import dj_database_url
import cartoview

INSTALLED_APPS += ("cartoview",
                   "cartoview.cartoview_api.apps.CartoviewAPIConfig",
                   "cartoview.app_manager", "cartoview.site_management",
                   "cartoview.apps_handler.apps.AppsHandlerConfig")
ROOT_URLCONF = "cartoview.urls"
CARTOVIEW_DIR = os.path.abspath(os.path.dirname(cartoview.__file__))
BASE_DIR = os.path.dirname(CARTOVIEW_DIR)
# CARTOVIEW_TEMPLATE_DIRS = [os.path.join(CARTOVIEW_DIR, "templates")
#                            ] + TEMPLATES[0]["DIRS"]
# TEMPLATES[0]["DIRS"] = CARTOVIEW_TEMPLATE_DIRS
CARTOVIEW_STATIC_DIRS = [
    os.path.join(CARTOVIEW_DIR, "static"),
]
STATICFILES_DIRS += CARTOVIEW_STATIC_DIRS
APPS_DIR = os.path.abspath(os.path.join(CARTOVIEW_DIR, "apps"))
PENDING_APPS = os.path.join(APPS_DIR, "pendingOperation.yml")
APPS_MENU = False
DOCKER = os.getenv('DOCKER', False)
CARTOVIEW_CONTEXT_PROCESSORS = [
    'cartoview.app_manager.context_processors.cartoview_processor',
    'cartoview.app_manager.context_processors.site_logo'
]
TEMPLATES = [
    {
        'NAME': 'GeoNode Project Templates',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(CARTOVIEW_DIR, "templates"), os.path.join(PROJECT_ROOT, "templates")],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                # 'django.core.context_processors.debug',
                # 'django.core.context_processors.i18n',
                # 'django.core.context_processors.tz',
                # 'django.core.context_processors.media',
                # 'django.core.context_processors.static',
                # 'django.core.context_processors.request',
                'geonode.context_processors.resource_urls',
                'geonode.geoserver.context_processors.geoserver_urls',
            ]+CARTOVIEW_CONTEXT_PROCESSORS,
            # Either remove APP_DIRS or remove the 'loaders' option.
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'cartoview.app_manager.loaders.Loader',
            ],
            'debug': DEBUG,
        },
    },
]
# TEMPLATES[0]["OPTIONS"]['context_processors'] += CARTOVIEW_CONTEXT_PROCESSORS
# TEMPLATES[0]["OPTIONS"]['loaders'] = [
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#     'cartoview.app_manager.loaders.Loader'
# ],
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

if 'datastore' in DATABASES:
    OGC_SERVER['default']['DATASTORE'] = 'datastore'

if 'geonode.geoserver' in INSTALLED_APPS and "LOCAL_GEOSERVER" in \
        locals() and LOCAL_GEOSERVER in MAP_BASELAYERS:
    LOCAL_GEOSERVER["source"][
        "url"] = OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms"

# NOTE:set cartoview_stand_alone environment var if you are not using cartoview_proect_template
CARTOVIEW_STAND_ALONE = strtobool(os.getenv('CARTOVIEW_STAND_ALONE', 'FALSE'))
if CARTOVIEW_STAND_ALONE:
    from cartoview.app_manager.settings import load_apps
    INSTALLED_APPS += load_apps()
