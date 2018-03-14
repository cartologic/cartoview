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
                    importlib.import_module(app_name)
                    app = App(title=app_name, name=app_name, status="Alpha", license=None,
                              version='1.0.0', installed_by=user, store=None, single_instance=False)
                    single = False
                    try:
                        installer = importlib.import_module(
                            '%s.installer' % app_name)
                        single = installer.info.get('single_instance', False)
                    except:
                        print(
                            '%-15s installer.py not found so this app will be marked as Multiple Instance' % (app_name))
                    app.single_instance = single
                    app.save()
                    category, created = AppType.objects.get_or_create(
                        name='app_manager_loader')
                    
                    app.category.add(category)
                    app.tags.add(*['cartoview', ])
                    app.save()
                    print('%-15s loaded Successfully' % (app_name))
                except Exception as e:
                    print('Failed to load %-5s may be app folder not found error: %-10s' %
                          (app_name, e.message))
