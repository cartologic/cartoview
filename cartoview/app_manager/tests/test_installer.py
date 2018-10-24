import threading

from django.contrib.admin import ACTION_CHECKBOX_NAME
from django.core.urlresolvers import reverse
from django.test import TestCase

from cartoview.app_manager.installer import AppInstaller
from cartoview.app_manager.models import App
from geonode.people.models import Profile

lock = threading.RLock()


class AppInstallerTest(TestCase):
    fixtures = ['sample_admin.json', 'app_stores.json']

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_app_installer(self):
        with lock:
            user = Profile.objects.filter(is_superuser=True).first()
            store_id = 1
            app_name = "cartoview_dashboard"
            app_version = "1.4.2"
            app_installer = AppInstaller(app_name, store_id, app_version, user)
            installed_apps = app_installer.install()
            self.assertEqual(len(installed_apps), 1)
            apps_admin_url = reverse(
                "admin:%s_%s_changelist" % (App._meta.app_label,
                                            App._meta.model_name))
            data = {
                'action': 'suspend_selected',
                ACTION_CHECKBOX_NAME:
                [unicode(app.pk) for app in installed_apps]
            }
            resp = self.client.post(apps_admin_url, data)
            self.assertNotEqual(resp.status_code, 500)
            data = {
                'action': 'activate_selected',
                ACTION_CHECKBOX_NAME:
                [unicode(app.pk) for app in installed_apps]
            }
            resp = self.client.post(apps_admin_url, data)
            self.assertNotEqual(resp.status_code, 500)
            uninstalled = app_installer.uninstall()
            self.assertEqual(uninstalled, True)

    def tearDown(self):
        pass
