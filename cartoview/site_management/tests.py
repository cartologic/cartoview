from __future__ import print_function
import os

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files.images import ImageFile
from django.test import TestCase
from django.test.utils import override_settings

from cartoview.site_management.models import SiteLogo


@override_settings(SITE_NAME='Test_Example')
@override_settings(SITE_ID=1)
class SiteManagementTest(TestCase):

    def setUp(self):
        self.site = Site.objects.first()

    def test_create_site_logo(self):
        logo_path = os.path.join(settings.CARTOVIEW_DIR, "static",
                                 "cartoview", "img", "cartoview-logo.png")
        logo = ImageFile(open(logo_path, "rb"), 'cartoview_logo.png')
        site_logo = SiteLogo.objects.create(site=self.site, logo=logo)
        self.assertIsNotNone(site_logo)
        print(site_logo.__str__())
