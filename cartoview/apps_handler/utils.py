# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from django.conf import settings
from future import standard_library

from cartoview.app_manager.helpers import (change_path_permission,
                                           create_direcotry)

standard_library.install_aliases()


def create_apps_dir(apps_dir):
    if not apps_dir:
        apps_dir = getattr(settings, 'APPS_DIR', None)
    if not apps_dir:
        project_dir = getattr(settings, 'BASE_DIR', settings.PROJECT_DIR)
        apps_dir = os.path.abspath(os.path.join(
            os.path.dirname(project_dir), "apps"))
    if not os.path.exists(apps_dir):
        create_direcotry(apps_dir)
        if not os.access(apps_dir, os.W_OK):
            change_path_permission(apps_dir)
