# -*- coding: utf-8 -*-
import cartoview
import geonode
from geonode.settings import *
import os
INSTALLED_APPS += ("cartoview", "cartoview.app_manager",
                   "cartoview.user_engage", "cartoview.workspace")
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
WORKSPACE_ENABLED = True
TEMPLATES[0]["OPTIONS"]['context_processors'] += (
    'cartoview.app_manager.context_processors.apps',
    'cartoview.app_manager.context_processors.news',
    'cartoview.app_manager.context_processors.apps_instance',
    'cartoview.app_manager.context_processors.site_logo',
    'cartoview.app_manager.context_processors.apps_menu',
    'cartoview.app_manager.context_processors.workspace')
execfile(cartoview_apps_settings_path)
