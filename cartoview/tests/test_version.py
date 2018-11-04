import os

import dj_database_url
import gisdata
from django.conf import settings
from django.test.testcases import LiveServerTestCase
from django.test.utils import override_settings
from geonode.layers.models import Layer
from geonode.layers.utils import upload
from geonode.tests.utils import get_web_page

import timeout_decorator


class CartoviewTest(LiveServerTestCase):
    port = 8000
    fixtures = [
        'sample_admin.json',
        'default_oauth_apps.json',
    ]

    # @classmethod
    # def setUpClass(cls):
    # from geonode.celery_app import app
    # from django.db import connections
    # import threading
    #     super(CartoviewTest, cls).setUpClass()
    #     app.control.purge()
    #     cls._worker = app.Worker(app=app, pool='solo', concurrency=1)
    #     connections.close_all()
    #     cls._thread = threading.Thread(target=cls._worker.start)
    #     cls._thread.daemon = True
    #     cls._thread.start()

    # @classmethod
    # def tearDownClass(cls):
    #     cls._worker.stop()
    #     super(CartoviewTest, cls).tearDownClass()

    # def tearDown(self):
    #     super(CartoviewTest, self).tearDown()
    #     # move to original settings
    #     settings.OGC_SERVER['default']['DATASTORE'] = ''
    #     del settings.DATABASES['datastore']

    def setUp(self):
        super(CartoviewTest, self).setUp()
        settings.DATASTORE_URL = 'postgis://cartoview:cartoview@' +\
        'localhost:5432/cartoview_datastore'
        postgis_db = dj_database_url.parse(
            settings.DATASTORE_URL, conn_max_age=600)
        settings.DATABASES['datastore'] = postgis_db
        settings.OGC_SERVER['default']['DATASTORE'] = 'datastore'

    @override_settings(
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        CELERY_ALWAYS_EAGER=True,
        BROKER_BACKEND='memory')
    @timeout_decorator.timeout(6000)
    def test_layer_upload(self):
        layers = {}
        expected_layers = []
        not_expected_layers = []

        for filename in os.listdir(gisdata.GOOD_DATA):
            basename, extension = os.path.splitext(filename)
            if extension.lower() in ['.tif', '.shp', '.zip']:
                expected_layers.append(
                    os.path.join(gisdata.GOOD_DATA, filename))

        for filename in os.listdir(gisdata.BAD_DATA):
            not_expected_layers.append(
                os.path.join(gisdata.BAD_DATA, filename))
        uploaded = upload(gisdata.DATA_DIR, console=None)

        for item in uploaded:
            errors = 'error' in item
            if errors:
                if item['file'] in not_expected_layers:
                    continue
                else:
                    msg = ('Could not upload file "%s", '
                           'and it is not in %s' % (item['file'],
                                                    not_expected_layers))
                    assert errors, msg
            else:
                msg = ('Upload should have returned either "name" or '
                       '"errors" for file %s.' % item['file'])
                assert 'name' in item, msg
                layers[item['file']] = item['name']

        msg = ('There were %s compatible layers in the directory,'
               ' but only %s were sucessfully uploaded' %
               (len(expected_layers), len(layers)))

        for layer in expected_layers:
            msg = ('The following file should have been uploaded'
                   'but was not: %s. ' % layer)
            assert layer in layers, msg

            layer_name = layers[layer]
            Layer.objects.get(name=layer_name)
            found = False
            gs_username, gs_password = settings.OGC_SERVER['default'][
                'USER'], settings.OGC_SERVER['default']['PASSWORD']
            page = get_web_page(
                os.path.join(settings.OGC_SERVER['default']['LOCATION'],
                             'rest/layers'),
                username=gs_username,
                password=gs_password)
            if page.find('rest/layers/%s.html' % layer_name) > 0:
                found = True
            if not found:
                msg = (
                    'Upload could not be verified, the layer %s is not '
                    'in geoserver %s, but GeoNode did not raise any errors, '
                    'this should never happen.' %
                    (layer_name, settings.OGC_SERVER['default']['LOCATION']))
                raise Exception(msg)
        for layer in expected_layers:
            layer_name = layers[layer]
            Layer.objects.get(name=layer_name).delete()
