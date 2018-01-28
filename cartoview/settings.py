# -*- coding: utf-8 -*-
import os

import cartoview
import geonode
from geonode.settings import *

INSTALLED_APPS += ("cartoview",
                   "cartoview.cartoview_api.apps.CartoviewAPIConfig",
                   "cartoview.app_manager", "cartoview.site_management")
ROOT_URLCONF = "cartoview.urls"
CARTOVIEW_ROOT = os.path.abspath(os.path.dirname(cartoview.__file__))
GEONODE_ROOT = os.path.abspath(os.path.dirname(geonode.__file__))
TEMPLATES[0]["DIRS"] = [os.path.join(CARTOVIEW_ROOT, "templates")
                        ] + TEMPLATES[0]["DIRS"]
STATICFILES_DIRS += [
    os.path.join(CARTOVIEW_ROOT, "static"),
]
cartoview_apps_settings_path = os.path.join(CARTOVIEW_ROOT, 'app_manager',
                                            "settings.py")
APPS_MENU = False
DOCKER = os.getenv('DOCKER', False)
TEMPLATES[0]["OPTIONS"]['context_processors'] += (
    'cartoview.app_manager.context_processors.cartoview_processor',
    'cartoview.app_manager.context_processors.site_logo',)
execfile(cartoview_apps_settings_path)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'full': {
            'format': '[%(asctime)s] %(module)s p%(process)s  { %(name)s %(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
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
