from django.test import TestCase
import mock
from .models import AppTag
# Create your tests here.
from django.core.management import call_command


class AppTagsTestCase(TestCase):

    def test_AppTag(self):
        mock_instance = mock.Mock(spec=AppTag)
        mock_instance.name = "maps"
        mock_instance.__str__ = mock.Mock(return_value=mock_instance.name)
        self.assertEqual(AppTag.__str__(mock_instance),
                         mock_instance.__str__())
