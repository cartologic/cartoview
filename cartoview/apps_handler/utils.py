from django.conf import settings
import os

from cartoview.app_manager.helpers import (change_path_permission,
                                           create_direcotry)


def create_apps_dir(apps_dir=getattr(settings, 'APPS_DIR', None)):
    if not apps_dir:
        project_dir = getattr(settings, 'BASE_DIR', settings.PROJECT_DIR)
        apps_dir = os.path.abspath(os.path.join(
            os.path.dirname(project_dir), "apps"))
    if not os.path.exists(apps_dir):
        create_direcotry(apps_dir)
        if not os.access(apps_dir, os.W_OK):
            change_path_permission(apps_dir)
