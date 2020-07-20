from __future__ import print_function

import requests
from django.core.management.base import BaseCommand

from cartoview.app_manager.installer import AppJson, remove_unwanted
from cartoview.app_manager.models import App
from cartoview.store_api.api import StoreAppResource


class Command(BaseCommand):
    help = 'Update existing apps'

    def handle(self, *args, **options):
        # stores = AppStore.objects.filter(is_default=True)
        # store = stores.first()
        for index, app in enumerate(App.objects.all()):
            try:
                if app.store:
                    data = self.get_data_from_store(app.name, app.store.url)
                    api_obj = StoreAppResource()
                    bundle = api_obj.build_bundle(data=data)
                    app_obj = api_obj.obj_get(bundle)
                    data = app_obj
                    app_serializer = AppJson(remove_unwanted(data))
                    app = app_serializer.get_app_object(app)
                    app.save()
                    print('[%-2s] %-35s  updated' % (index + 1, app.name))
                else:
                    print('[%-2s] %-35s  Ignored because No Store Available' %
                          (index + 1, app.name))
            except Exception as ex:
                print('[%-2s] %-35s  Failed error message %-25s' %
                      (index + 1, app.name, ex))

    def get_data_from_store(self, appname, url):
        payload = {'name__exact': appname}
        req = requests.get(url + "app", params=payload)
        json_api = req.json()
        app_data = json_api.get('objects')[0]
        return app_data
