from django.conf import settings
from django.test import TestCase
from faker import Faker

from cartoview.cartoview_api.views import (
    get_geoserver_credintials, convert_infinty)


class CartoviewApiViewsTest(TestCase):
    def setUp(self):
        self.faker = Faker()

    def test_get_geoserver_credintials(self):
        gs_user, gs_password, gs_url = get_geoserver_credintials()
        self.assertEqual(gs_user, settings.OGC_SERVER_DEFAULT_USER)
        self.assertEqual(gs_password, settings.OGC_SERVER_DEFAULT_PASSWORD)
        self.assertEqual(gs_url, settings.GEOSERVER_LOCATION)

    def test_convert_infinty(self):
        self.assertIsNone(convert_infinty(float('inf')))
        self.assertIsNotNone(convert_infinty(self.faker.random.random()))
        self.assertIsNotNone(convert_infinty(self.faker.name()))
        self.assertIsNotNone(convert_infinty(self.faker.text()))
