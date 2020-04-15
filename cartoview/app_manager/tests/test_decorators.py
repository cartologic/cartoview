from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.http import HttpRequest
from django.test import TestCase
from geonode.people.models import Profile
from mock import Mock

from cartoview.app_manager.decorators import can_view_app_instance
from cartoview.app_manager.models import App, AppInstance


class DecoratorsTest(TestCase):
    fixtures = ['sample_admin.json', ]

    def setUp(self):
        call_command("load_current_apps")
        self.app = App.objects.get(name="cartoview_basic_viewer")
        self.app_instance = AppInstance()
        self.app_instance.app = self.app
        self.user = Profile.objects.get(username="admin")
        self.app_instance.owner = self.user
        self.app_instance.title = "fake_viewer"
        self.app_instance.config = {}
        self.app_instance.abstract = "fake_viewer_abstract"
        self.app_instance.map_id = None
        self.app_instance.save()

    def test_can_view_app(self):
        func_allowed = Mock()
        func_allowed.__name__ = "fake_app_view"
        req = HttpRequest()
        req.user = self.user
        decorated = can_view_app_instance(func_allowed)
        decorated(req, instance_id=self.app_instance.id)
        self.assertTrue(func_allowed.called)
        func_anonymous_allowed = Mock()
        func_anonymous_allowed.__name__ = "fake_app_view"
        req.user = AnonymousUser()
        decorated = can_view_app_instance(func_anonymous_allowed)
        decorated(req, instance_id=self.app_instance.id)
        self.assertTrue(func_anonymous_allowed.called)
        func_not_allowed = Mock()
        func_not_allowed.__name__ = "fake_app_view"
        decorated = can_view_app_instance(func_not_allowed)
        owner_permissions = [
            'view_resourcebase',
            'download_resourcebase',
            'change_resourcebase_metadata',
            'change_resourcebase',
            'delete_resourcebase',
            'change_resourcebase_permissions',
            'publish_resourcebase',
        ]
        permessions = {
            'users': {
                '{}'.format(self.user): owner_permissions,
            }
        }
        self.app_instance.set_permissions(permessions)
        try:
            decorated(req, instance_id=self.app_instance.id)
        except PermissionDenied:
            pass
        self.assertFalse(func_not_allowed.called)
