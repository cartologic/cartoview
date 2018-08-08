from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from django.core.urlresolvers import reverse
from cartoview.cartoview_api.rest import ExtendedResourceBaseResource
from geonode.urls import api


class ExtendedResourceBaseResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['sample_admin.json']

    def setUp(self):
        super(ExtendedResourceBaseResourceTest, self).setUp()
        self.username = 'admin'
        self.password = 'admin'

    def get_credentials(self):
        return self.create_basic(
            username=self.username,
            password=self.password)

    def test_get_list(self):
        target_url = reverse(
            "api_dispatch_list",
            kwargs={"resource_name":
                    ExtendedResourceBaseResource.Meta.resource_name,
                    "api_name": api.api_name})
        self.assertHttpOK(self.api_client.get(
            target_url, format='json'))
