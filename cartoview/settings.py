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
from pre_settings import *

import geonode
from geonode.settings import *

#
# General Django development settings
#

SITENAME = 'cartoview'

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
GEONODE_ROOT = os.path.abspath(os.path.dirname(geonode.__file__))
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


MIDDLEWARE_CLASSES = (
    'cartoview.middleware.LimitDomainsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # The setting below makes it possible to serve different languages per
    # user depending on things like headers in HTTP requests.
    'django.middleware.locale.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # This middleware allows to print private layers for the users that have
    # the permissions to view them.
    # It sets temporary the involved layers as public before restoring the permissions.
    # Beware that for few seconds the involved layers are public there could be risks.
    # 'geonode.middleware.PrintProxyMiddleware',
)

print MIDDLEWARE_CLASSES
# Add cartoview.app_manager to INSTALLED_APPS before GEONODE_APPS to ovrride the template tag 'base_tags' of geonode
INSTALLED_APPS = tuple(i for i in INSTALLED_APPS if i not in GEONODE_APPS)
INSTALLED_APPS += ('bootstrap3', 'south', 'corsheaders',)
INSTALLED_APPS += ('cartoview', 
    'cartoview.app_manager', 
    # 'cartoview.viewer', 
    'cartoview.basic.geonode_map_application',)
INSTALLED_APPS += GEONODE_APPS
CARTOVIEW_APPS = ()
# auto load apps
import sys, importlib

APPS_DIR = os.path.abspath(os.path.join(CARTOVIEW_ROOT, os.pardir, "apps"))
print APPS_DIR
apps_names = [n for n in os.listdir(APPS_DIR) if os.path.isdir(os.path.join(APPS_DIR, n))]
sys.path.append(APPS_DIR)
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

# define the urls after the settings are overridden
if 'geonode.geoserver' in INSTALLED_APPS:
    MAP_BASELAYERS.remove(LOCAL_GEOSERVER)
    LOCAL_GEOSERVER = {
        "source": {
            "ptype": "gxp_wmscsource",
            "url": OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms",
            "restUrl": "/gs/rest"
        }
    }
    baselayers = MAP_BASELAYERS
    MAP_BASELAYERS = [LOCAL_GEOSERVER]
    MAP_BASELAYERS.extend(baselayers)

    # Uncomment this line incase a restart server batch exists.
    # RESTART_SERVER_BAT = "<full_path>/restart_server.bat"

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

TASTYPIE_ALLOW_MISSING_SLASH = True

PROXY_ALLOWED_HOSTS = ('*',)