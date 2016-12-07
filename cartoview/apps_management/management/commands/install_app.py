import os
import requests
import tempfile
import shutil
import re
from django.core.management.base import BaseCommand, CommandError
import pkg_resources
import subprocess
from django.conf import settings

from cartoview.apps_management.models import InstalledApps, AppStore

reload(pkg_resources)
REST_URL = AppStore.objects.all()[0].url


def dep_install(self, dep_list):
    for i, x in enumerate(dep_list):
        if i == len(dep_list):
            return
        else:
            for x in dep_list:
                q = requests.get(REST_URL + 'app/?name={}'.format(x))
                app_name = q.json()['objects'][0]['name']
                if q.json()['objects'][0]['latest_version']["dependencies"]:
                    dep_install(self, q.json()['objects'][0]['latest_version']["dependencies"])
                    install_app(self, app_name)
                else:
                    install_app(self, app_name)


def install_app(self, app_slug):
    r = requests.get('http://127.0.0.1:8000/apps/update_download/{}'.format(app_slug), stream=True)
    d = r.headers['content-disposition']
    file_name = re.findall("filename=(.+)", d)[0]
    download_path = tempfile.mkdtemp()
    file_path = os.path.join(download_path, file_name)
    with open(file_path, 'wb+') as out_file:
        shutil.copyfileobj(r.raw, out_file)
    process = subprocess.Popen("{}\pip.exe install {}".format(settings.PIP_PATH, file_path), shell=True,
                               stdout=subprocess.PIPE)
    process.wait()
    code = process.returncode
    if code == 0:
        app = InstalledApps.objects.filter(name=app_slug)
        if app.exists():
            app.delete()
        reload(pkg_resources)
        v = pkg_resources.get_distribution(app_slug).version
        InstalledApps.objects.create(name=app_slug, version=v)
        shutil.rmtree(download_path)
        self.stdout.write("1")


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('app_slug', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        **status_code
        -0 means this app requires a hiegher cartoview version
        -1 means this app installed successfully
        -2 means this app requires another app which not installed
        """
        for app_slug in options['app_slug']:
            try:
                r = requests.get(REST_URL + 'app/?name={}'.format(app_slug))
                if r.json()['objects'][0]['latest_version']['dependencies']:
                    dep_install(self, r.json()['objects'][0]['latest_version']['dependencies'])
                    install_app(self, app_slug)
                else:
                    install_app(self, app_slug)
            except Exception, e:
                raise CommandError('error : {}'.format(str(e)))
                # import cartoview
                # from cartoview.apps_management.models import InstalledApps
                # installed_packages = [app._key for app in pip.get_installed_distributions()]
                # reload module to ensure detecting changes
