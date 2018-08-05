from django.test import TestCase
from geonode.people.models import Profile
from cartoview.app_manager.models import AppStore
from cartoview.app_manager.installer import AppInstaller
from django.conf import settings
import shutil
import os
from cartoview.app_manager.helpers import create_direcotry
from cartoview.log_handler import get_logger
logger = get_logger(__name__)


class AppInstallerTest(TestCase):
    fixtures = ['sample_admin.json']

    def setUp(self):
        AppStore.objects.create(
            name="Test Store", url="https://appstore.cartoview.net/api/v1/",
            is_default=True)

    def test_app_installer(self):
        user = Profile.objects.filter(is_superuser=True).first()
        store_id = 1
        app_name = "cartoview_basic_viewer"
        app_version = "1.7.9"
        installer = AppInstaller(app_name, store_id, app_version, user)
        installed_apps = installer.install()
        logger.debug(installed_apps)
        self.assertEqual(len(installed_apps), 1)
        uninstalled = installer.uninstall()
        logger.debug(uninstalled)
        self.assertEqual(uninstalled, True)

    def tearDown(self):
        shutil.rmtree(settings.APPS_DIR)
