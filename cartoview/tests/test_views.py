import json

import requests
from django.urls import reverse
from django.test import TestCase
from geonode.urls import api
from pkg_resources import parse_version

from cartoview.version import get_current_version


class CartoviewHomeViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')


class CartoviewCheckVersionViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/check-version/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('check_version'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('check_version'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cartoview/check_version.js')
        self.assertEqual("current_version" in resp.context, True)
        self.assertEqual("latest_version" in resp.context, True)
        _version = parse_version(get_current_version())._version
        release = _version.release
        version = [str(x) for x in release]
        current_version = ".".join(version)
        req = requests.get("https://pypi.org/pypi/cartoview/json")
        latest_version = str(req.json()["info"]["version"])
        self.assertEqual(resp.context["current_version"], current_version)
        self.assertEqual(resp.context["latest_version"], latest_version)


class CartoviewResourcesRegisteredTest(TestCase):

    def test_api_url_exists_at_desired_location(self):
        resp = self.client.get('/api/')
        self.assertEqual(resp.status_code, 200)

    def test_api_url_accessible_by_name(self):
        resp = self.client.get(
            reverse("api_%s_top_level" % api.api_name,
                    kwargs={"api_name": api.api_name}))
        self.assertEqual(resp.status_code, 200)

    def test_cartoview_resources_exists(self):
        resp = self.client.get(
            reverse("api_%s_top_level" % api.api_name,
                    kwargs={"api_name": api.api_name}))
        self.assertEqual(resp.status_code, 200)
        resources_dict = json.loads(resp.content)
        self.assertTrue("app" in resources_dict.keys())
        self.assertTrue("appinstances" in resources_dict.keys())
        self.assertTrue("all_resources" in resources_dict.keys())
        for endpoint in resources_dict.values():
            resp = self.client.get(endpoint['list_endpoint'])
            self.assertEqual(resp.status_code, 200)
