import importlib

from django.core.management.base import BaseCommand
from geonode.people.models import Profile

from cartoview.app_manager.models import App, AppType
from cartoview.apps_handler.config import CartoviewApp
from cartoview.log_handler import get_logger

logger = get_logger(with_formatter=True)


class Command(BaseCommand):
    help = 'Update existing apps'

    def handle(self, *args, **options):
        carto_apps = CartoviewApp.objects.get_active_apps().values()
        user = Profile.objects.filter(is_superuser=True).first()
        for carto_app in carto_apps:
            app_name = carto_app.name
            query = App.objects.filter(name=app_name)
            if query.count() == 0:
                try:
                    # ensure that the folder is python module
                    importlib.import_module(app_name)
                    app = App(
                        title=app_name,
                        name=app_name,
                        status="Alpha",
                        license=None,
                        version='1.0.0',
                        installed_by=user,
                        store=None,
                        order=carto_app.order,
                        single_instance=False)
                    single = False
                    try:
                        installer = importlib.import_module(
                            '%s.installer' % app_name)
                        single = getattr(installer.info, 'single_instance',
                                         False)
                    except BaseException:
                        logger.error(
                            ('%-15s installer.py not found so this app will ' +
                             'be marked as Multiple Instance') % (app_name))
                    app.single_instance = single
                    app.save()
                    category, created = AppType.objects.get_or_create(
                        name='app_manager_loader')

                    app.category.add(category)
                    app.tags.add(*[
                        'cartoview',
                    ])
                    app.save()
                    logger.info('%-15s loaded Successfully' % (app_name))
                except Exception as e:
                    logger.error(('Failed to load %-5s may be ' +
                                  'app folder not found error: %-10s') %
                                 (app_name, e))
