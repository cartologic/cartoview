import os
import shutil

from django.conf import settings
from django.test import TestCase

from cartoview.app_manager.helpers import (
    get_path_permission, get_perm, make_writeable_recursive, create_direcotry)


class HelpersTest(TestCase):
    def test_helpers(self):
        apps_dir_perm = get_perm(settings.APPS_DIR)
        self.assertEqual(apps_dir_perm, 511)
        apps_dir_perm = get_path_permission(settings.APPS_DIR)
        self.assertEqual(apps_dir_perm, ('0o777', '0o777'))
        try:
            make_writeable_recursive(settings.APPS_DIR)
        except OSError:
            self.fail("Failed to change permission")
        test_dir = os.path.join(settings.CARTOVIEW_DIR, 'test_dir')
        create_direcotry(test_dir)
        self.assertTrue(os.path.exists(test_dir))
        shutil.rmtree(test_dir)
