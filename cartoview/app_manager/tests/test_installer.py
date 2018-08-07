import os
import shutil
import threading

from django.conf import settings
from django.test import TestCase
from geonode.people.models import Profile

from cartoview.app_manager.helpers import create_direcotry
from cartoview.app_manager.installer import AppInstaller
from cartoview.app_manager.models import AppStore

lock = threading.RLock()


class AppInstallerTest(TestCase):
    fixtures = ['sample_admin.json', 'app_stores.json']

    def setUp(self):
        pass

    def test_app_installer(self):
        with lock:
            user = Profile.objects.filter(is_superuser=True).first()
            store_id = 1
            app_name = "cartoview_tutorials"
            app_version = "0.1.4"
            app_installer = AppInstaller(app_name, store_id, app_version, user)
            installed_apps = app_installer.install()
            self.assertEqual(len(installed_apps), 1)
            uninstalled = app_installer.uninstall()
            self.assertEqual(uninstalled, True)

    def tearDown(self):
        pass
