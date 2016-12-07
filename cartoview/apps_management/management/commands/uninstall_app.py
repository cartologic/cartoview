from django.core.management.base import BaseCommand, CommandError
from cartoview.apps_management.models import InstalledApps
import subprocess
from django.conf import settings


# pip_path = "C:\Users\CartoLogic\Desktop\managerenv\Scripts"


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('app_slug', nargs='+', type=str)

    def handle(self, *args, **options):
        for app_slug in options['app_slug']:
            try:
                process = subprocess.Popen("{}\pip.exe uninstall {} -y".format(settings.PIP_PATH, app_slug), shell=True,
                                           stdout=subprocess.PIPE)
                process.wait()
                code = process.returncode
                if code == 0:
                    InstalledApps.objects.filter(name=app_slug).delete()
                    self.stdout.write("0")
                else:
                    self.stdout.write("1")
            except Exception, e:
                raise CommandError('error : {}'.format(str(e)))
