# -*- coding: utf-8 -*-
import os
from distutils.util import strtobool

from geonode.settings import *

import cartoview

INSTALLED_APPS += ("cartoview",
                   "cartoview.cartoview_api.apps.CartoviewAPIConfig",
                   "cartoview.app_manager", "cartoview.site_management",
                   "cartoview.apps_handler.apps.AppsHandlerConfig")
ROOT_URLCONF = "cartoview.urls"
CARTOVIEW_DIR = os.path.abspath(os.path.dirname(cartoview.__file__))
BASE_DIR = os.path.dirname(CARTOVIEW_DIR)
TEMPLATES[0]["DIRS"] = [os.path.join(CARTOVIEW_DIR, "templates")
                        ] + TEMPLATES[0]["DIRS"]
STATICFILES_DIRS += [
    os.path.join(CARTOVIEW_DIR, "static"),
]
APPS_DIR = os.path.abspath(os.path.join(CARTOVIEW_DIR, "apps"))
PENDING_APPS = os.path.join(APPS_DIR, "pendingOperation.yml")
APPS_MENU = False
DOCKER = os.getenv('DOCKER', False)
TEMPLATES[0]["OPTIONS"]['context_processors'] += (
    'cartoview.app_manager.context_processors.cartoview_processor',
    'cartoview.app_manager.context_processors.site_logo'
)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'full': {
            'format':
            '[%(asctime)s] %(module)s p%(process)s  { %(name)s %(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'full'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        }
    }
}
# bower static files
STATICFILES_DIRS += [
    os.path.join(CARTOVIEW_DIR, "static"),
]
# django Media Section
# uncomment the following if you want your files out of geonode folder
MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded")
MEDIA_URL = "/uploaded/"
LOCAL_MEDIA_URL = "/uploaded/"
CKEDITOR_UPLOAD_PATH = "uploads/"
# static section
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# INSTALLED_APPS = ('ckeditor', ) + INSTALLED_APPS
# INSTALLED_APPS += ('hazards', 'gpkg_manager', "ags2sld")
try:
    from .local_settings import *
except Exception as e:
    print e.message

if 'datastore' in DATABASES:
    OGC_SERVER['default']['DATASTORE'] = 'datastore'

if 'geonode.geoserver' in INSTALLED_APPS and "LOCAL_GEOSERVER" in \
        locals() and LOCAL_GEOSERVER in MAP_BASELAYERS:
    LOCAL_GEOSERVER["source"][
        "url"] = OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms"
# NOTE:set cartoview_stand_alone environment var if you are not using cartoview_proect_template
if strtobool(os.getenv('cartoview_stand_alone', 'FALSE')):
    from cartoview.app_manager.settings import load_apps
    INSTALLED_APPS += load_apps()
