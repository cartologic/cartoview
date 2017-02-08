import os
import re
import shutil
import zipfile
import tempfile
import requests
import importlib
import pkg_resources
from StringIO import StringIO
from .models import AppStore, App, AppTag
from django.db.models import Max, Min, F
from collections import OrderedDict
from django.apps import apps
from django.conf import settings
from django.core import management
from .config import App as AppConfig, AppsConfig
reload(pkg_resources)


current_folder = os.path.abspath(os.path.dirname(__file__))
temp_dir = os.path.join(current_folder, 'temp')

class AppAlreadyInstalledException(BaseException):
    message = "Application is already installed."


class AppInstaller:
    """

    """
    def __init__(self, name, store_id=None, version=None):
        self.app_dir = os.path.join(settings.APPS_DIR, name)
        self.name = name
        if store_id is None:
            self.store = AppStore.objects.get(is_default=True)
        else:
            self.store = AppStore.objects.get(id=store_id)
        self.info = self._request_rest_data("app/?name=", name)['objects'][0]
        if version is None or version == 'latest' or self.info["latest_version"]["version"] == version:
            self.version = self.info["latest_version"]
        else:
            data = self._request_rest_data("appversion/?app__name=", name, "&version=", version)
            self.version = data['objects'][0]

    def _request_rest_data(self, *args):
        """
        get app information form app store rest url
        """
        try:
            q = requests.get(self.store.url + ''.join([str(item) for item in args]))
            return q.json()
        except:
            return None

    def _download_app(self):
        response = requests.get(self.version["download_link"], stream=True)
        zip_ref = zipfile.ZipFile(StringIO(response.content))
        try:
            # extract_to = os.path.join(settings.APPS_DIR)
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            extract_to = tempfile.mkdtemp(dir=temp_dir)
            zip_ref.extractall(extract_to)
            if self.upgrade and os.path.exists(self.app_dir):
                # move old version to temporary dir so that we can restore in case of failure
                old_version_temp_dir = tempfile.mkdtemp(dir=temp_dir)
                shutil.move(self.app_dir, old_version_temp_dir)
            self.old_app_temp_dir = os.path.join(extract_to, self.name)
            shutil.move(self.old_app_temp_dir, settings.APPS_DIR)
            # delete temp extract dir
            shutil.rmtree(extract_to)
        finally:
            zip_ref.close()
    
    def add_app(self, installer):

        # save app configuration
        info = installer.info
        app, created = App.objects.get_or_create(name=self.name)
        if created:
            app_config = AppConfig(name=self.name, active=True)
            app.apps_config.append(app_config)
            app.apps_config.save()
            app.order = app_config.order

        app.title = info.get('title', self.name)
        app.description = info.get('description', None)
        app.short_description = info.get('short_description', None)
        app.owner_url = info.get('owner_url', None)
        app.help_url = info.get('help_url', None)
        app.author = info.get('author', None)
        app.author_website = info.get('author_website', None)
        app.home_page = info.get('home_page', None)
        app.license = info.get('licence', None)
        app.single_instance = info.get('single_instance', False)
        app.version = self.version["version"]
        app.save()
        tags = info.get('tags', [])
        for tag_name in tags:
            try:
                tag = AppTag(name=tag_name)
                tag.save()
                app.tags.add(tag)
            except:
                pass

        return app

    def install(self, restart=True):
        self.upgrade = False
        if os.path.exists(self.app_dir):
            installedApp = App.objects.get(name=self.name)
            if installedApp.version < self.version["version"]:
                self.upgrade = True
            else:
                raise AppAlreadyInstalledException()
        installedApps = []
        for name, version in self.version["dependencies"].items():
            # use try except because AppInstaller.__init__ will handle upgrade if version not match
            try:
                app_installer = AppInstaller(name, self.store.id, version)
                installedApps += app_installer.install(restart=False)
            except AppAlreadyInstalledException:
                pass
        self._download_app()
        reload(pkg_resources)
        try:
            installer = importlib.import_module('%s.installer' % self.name)
            installedApps.append(self.add_app(installer))
            installer.install()
            if restart:
                finalize_setup()
        except Exception as ex:
            print ex.message
        return installedApps

    def uninstall(self, restart=True):
        """
        angular.forEach(app.store.installedApps.objects, function(installedApp){
                var currentApp = appsHash[installedApp.name];
                if(dependents.indexOf(currentApp) == -1 && currentApp.latest_version.dependencies[app.name]){
                    dependents.push(currentApp)
                    _getDependents(currentApp, appsHash, dependents)
                }

            });

        :return:
        """
        installedApps = App.objects.all()
        for app in installedApps:
            app_installer = AppInstaller(app.name, self.store.id, app.version)
            dependencies = app_installer.version["dependencies"]
            if self.name in dependencies:
                app_installer.uninstall(restart=False)
        installer = importlib.import_module('%s.installer' % self.name)
        installer.uninstall()
        from django.contrib.contenttypes.models import ContentType
        ContentType.objects.filter(app_label=self.name).delete()
        app = App.objects.get(name=self.name)
        app.delete()


        app_config = app.apps_config.get_by_name(self.name)
        del app.apps_config[app_config]
        app.apps_config.save()

        app_dir = os.path.join(settings.APPS_DIR, self.name)
        shutil.rmtree(app_dir)
        if restart:
            finalize_setup()

def finalize_setup():
    install_app_batch = getattr(settings, 'CARTOVIEW_INSTALL_APP_BAT', None)
    if install_app_batch:
        def _finalize_setup():
            from subprocess import Popen
            working_dir = os.path.dirname(install_app_batch)
            log_file = os.path.join(working_dir, "install_app_log.txt")
            with open(log_file, 'a') as log:
                p = Popen(install_app_batch, stdout=log, stderr=log, shell=True, cwd=working_dir)
            # stdout, stderr = p.communicate()

        from threading import Timer
        timer = Timer(0.1, _finalize_setup)
        timer.start()


