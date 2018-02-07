from django.conf import settings
from cartoview.app_manager.config import AppsConfig
from cartoview.app_manager.models import App, AppType
from django.core.management.base import BaseCommand
import importlib
import os
from geonode.people.models import Profile


class Command(BaseCommand):
    help = 'Update existing apps'

    def handle(self, *args, **options):
        apps_file_path = os.path.join(settings.APPS_DIR, "apps.yml")
        apps_config = AppsConfig(apps_file_path)
        user = Profile.objects.filter(is_superuser=True).first()
        for app_config in apps_config:
            app_name = app_config.name
            query = App.objects.filter(name=app_name)
            if app_config.active and query.count() == 0:
                try:
                    # ensure that the folder is python module
                    app_module = importlib.import_module(app_name)
                    app = App()
                    app.title = app_name
                    app.name = app_name
                    app.status = "Alpha"
                    app.license = None
                    app.version = '1.0.0'
                    app.installed_by = user
                    app.store = None
                    single = False
                    try:
                        installer = importlib.import_module(
                            '%s.installer' % app_name)
                        single = installer.info.get('single_instance', False)
                    except:
                        print('{} installer.py not found so this app will be marked as Multiple Instance'.
                              format(app_name))
                    app.single_instance = single
                    app.save()
                    category, created = AppType.objects.get_or_create(
                        name='app_manager_loader')
                    app.category.add(category)
                    app.tags.add(*['cartoview', ])
                    app.save()
                    print('{} loaded Successfully'.
                          format(app_name))
                except Exception as e:
                    print('Failed to load {} may be app folder not found error: {}'.
                          format(app_name, e.message))
