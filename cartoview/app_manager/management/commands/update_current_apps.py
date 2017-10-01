from django.core.management.base import BaseCommand
import requests
from cartoview.app_manager.models import App, AppStore
from cartoview.app_manager.installer import AppSerializer
store = AppStore.objects.get(is_default=True)


class Command(BaseCommand):
    help = 'Update existing apps'

    def handle(self, *args, **options):
        for index, app in enumerate(App.objects.all()):
            try:
                data = self.get_data_from_store(app.name)
                app_serializer = AppSerializer(**data)
                app = app_serializer.get_app_object(app)
                app.save()
                print('[{}] {}  updated'.format(index + 1, app.name))
            except Exception as ex:
                print('[{}] {}  Failed error message {}'.format(
                    index + 1, app.name, ex.message))

    def get_data_from_store(self, appname):
        payload = {'name__exact': appname}
        req = requests.get(store.url + "app", params=payload)
        json_api = req.json()
        app_data = json_api.get('objects')[0]
        return app_data
