from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from cartoview.app_manager.models import (App, AppStore)


class UpdateCurrentAppsTest(TestCase):
    fixtures = ['app_stores.json', ]

    def test_command_output(self):
        out = StringIO()
        out1 = StringIO()
        call_command("load_current_apps", stdout=out1)
        call_command('update_current_apps', stdout=out)
        self.assertIn('', out.getvalue())
        viewer = App.objects.get(name="cartoview_basic_viewer")
        viewer.store = AppStore.objects.get(is_default=True)
        viewer.save()
        call_command('update_current_apps', stdout=out)
        self.assertIn('', out.getvalue())
