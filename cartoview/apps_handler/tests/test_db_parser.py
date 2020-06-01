import os

from django.test import TestCase
from django.test import override_settings

from ..db_parser import get_db_url


class DBParserTest(TestCase):
    def test_get_db_url(self):
        from django.conf import settings
        base_dir = getattr(settings, 'BASE_DIR', '')
        sqlite_path = os.path.join(base_dir, 'test.db')
        databases = {
            'postgis': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'cartoview',
                'USER': 'docker',
                'PASSWORD': 'docker',
                'HOST': 'localhost',
                'PORT': '5432',
            },
            'sqlite': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': sqlite_path
            }
        }
        with override_settings(DATABASES=databases):
            self.assertEqual(
                get_db_url('sqlite'), 'sqlite://{}'.format(sqlite_path))
            self.assertEqual(
                get_db_url('postgis'),
                'postgis://docker:docker@localhost:5432/cartoview')
