# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

# Django settings for the GeoNode project.
import os

# uncomment below line if gdal paths is not set in system environment.
# os.environ['Path'] = r'C:/path/to/GDAL;' + os.environ['Path']
# os.environ['GEOS_LIBRARY_PATH'] = r'C:/path/to/GDAL/geos_c.dll'
# os.environ['GDAL_LIBRARY_PATH'] = r'C:/path/to/GDAL/gdal111.dll'

import geonode
from geonode.settings import *

#
# General Django development settings
#


SITENAME = 'cartoview'

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
GEONODE_ROOT = os.path.abspath(os.path.abspath(geonode.__file__))
CARTOVIEW_ROOT = LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

# Defines settings for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(LOCAL_ROOT, 'development.db'),
    },
    # vector datastore for uploads
    # 'datastore' : {
    #    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #    'NAME': '',
    #    'USER' : '',
    #    'PASSWORD' : '',
    #    'HOST' : '',
    #    'PORT' : '',
    # }
}

WSGI_APPLICATION = "cartoview.wsgi.application"

# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *
except ImportError:
    pass

# override Geonode media and static root
MEDIA_ROOT = os.path.join(LOCAL_ROOT, "uploaded")
STATIC_ROOT = os.path.join(LOCAL_ROOT, "static_root")

# Additional directories which hold static files
STATICFILES_DIRS.append(
    os.path.join(LOCAL_ROOT, "static"),
)

# Note that Django automatically includes the "templates" dir in all the
# INSTALLED_APPS, se there is no need to add maps/templates or admin/templates
TEMPLATE_DIRS = (
                    os.path.join(LOCAL_ROOT, "templates"),
                ) + TEMPLATE_DIRS

# Location of url mappings
ROOT_URLCONF = 'cartoview.urls'

# Location of locale files
LOCALE_PATHS = (
                   os.path.join(LOCAL_ROOT, 'locale'),
               ) + LOCALE_PATHS

# Add cartoview.app_manager to INSTALLED_APPS before GEONODE_APPS
INSTALLED_APPS = tuple(i for i in INSTALLED_APPS if i not in GEONODE_APPS)
INSTALLED_APPS += ('cartoview.app_manager', 'cartoview.apps')
INSTALLED_APPS += GEONODE_APPS

# auto load apps
from cartoview.app_manager.apps_helper import get_apps_names, APPS_DIR

CARTOVIEW_APPS = ()

import importlib, sys

# TODO: find better solution to get access to apps directly.
sys.path.append(os.path.abspath(os.path.join(LOCAL_ROOT, 'apps')))

for app_name in get_apps_names():
    try:
        CARTOVIEW_APPS += ('cartoview.apps.' + app_name,)
        # settings_module = importlib.import_module('apps.%s.settings' % app_name)
        app_settings_file = os.path.join(APPS_DIR, app_name, 'settings.py')
        if os.path.exists(app_settings_file):
            # By doing this instead of import, app/settings.py can refer to
            # local variables from settings.py without circular imports.
            execfile(app_settings_file)
    except:
        pass

INSTALLED_APPS += CARTOVIEW_APPS

# Uncomment this line incase a restart server batch exists.
# RESTART_SERVER_BAT = "<full_path>/restart_server.bat"
