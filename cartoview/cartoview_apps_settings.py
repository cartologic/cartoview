# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
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

import os

from past.builtins import execfile

from cartoview import app_manager
from .settings import (
    INSTALLED_APPS,
    APPS_DIR
)

# Load CartoView Apps
app_manager_settings = os.path.join(
    os.path.dirname(app_manager.__file__),
    "settings.py"
)
execfile(os.path.realpath(app_manager_settings))
# load_apps method declared in app_manager_settings in the above line
load_apps(APPS_DIR)
INSTALLED_APPS += CARTOVIEW_APPS
for settings_file in APPS_SETTINGS:
    try:
        execfile(settings_file)
    except Exception as e:
        print(f'Error while importing {settings_file} : {e}')
