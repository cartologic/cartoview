# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib
import logging
import os
import shutil
import subprocess
import tempfile
import zipfile
from builtins import *
from builtins import object, str
from io import BytesIO
from sys import stdout
from threading import Timer

import pkg_resources
import requests
from django.conf import settings
from django.db.models import Max
from future import standard_library

from .config import App as AppConfig
from .models import App, AppStore, AppTag

standard_library.install_aliases()


reload(pkg_resources)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s  { %(name)s %(pathname)s:%(lineno)d} \
                            %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
current_folder = os.path.abspath(os.path.dirname(__file__))
temp_dir = os.path.join(current_folder, 'temp')


class AppAlreadyInstalledException(BaseException):
    message = "Application is already installed."


class AppInstaller(object):
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
        if version is None or version == 'latest' or self.info[
                "latest_version"]["version"] == version:
            self.version = self.info["latest_version"]
        else:
            data = self._request_rest_data("appversion/?app__name=", name,
                                           "&version=", version)
            self.version = data['objects'][0]

    def _request_rest_data(self, *args):
        """
        get app information form app store rest url
        """
        try:
            q = requests.get(self.store.url + ''.join(
                [str(item) for item in args]))
            return q.json()
        except BaseException as e:
            logger.error(e.message)
            return None

    def _download_app(self):
        response = requests.get(self.version["download_link"], stream=True)
        zip_ref = zipfile.ZipFile(
            BytesIO(response.content))
        try:
            # extract_to = os.path.join(settings.APPS_DIR)
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            extract_to = tempfile.mkdtemp(dir=temp_dir)
            zip_ref.extractall(extract_to)
            if self.upgrade and os.path.exists(self.app_dir):
                # move old version to temporary dir so that we can restore in
                # case of failure
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
            if app.order is None or app.order == 0:
                apps = App.objects.all()
                max_value = apps.aggregate(
                    Max('order'))['order__max'] if apps.exists() else 0
                app.order = max_value + 1
            app_config = AppConfig(
                name=self.name, active=True, order=app.order)
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
        app.store = AppStore.objects.filter(is_default=True).first()
        app.save()
        tags = info.get('tags', [])
        for tag_name in tags:
            tag, created = AppTag.objects.get_or_create(name=tag_name)
            app.tags.add(tag)
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
        for name, version in list(self.version["dependencies"].items()):
            # use try except because AppInstaller.__init__ will handle upgrade
            # if version not match
            try:
                app_installer = AppInstaller(name, self.store.id, version)
                installedApps += app_installer.install(restart=False)
            except AppAlreadyInstalledException as e:
                logger.error(e.message)
        self._download_app()
        reload(pkg_resources)
        try:
            installer = importlib.import_module('%s.installer' % self.name)
            installedApps.append(self.add_app(installer))
            installer.install()
            if restart:
                finalize_setup()
        except Exception as ex:
            logger.error(ex.message)
        return installedApps

    def uninstall(self, restart=True):
        """
        angular.forEach(app.store.installedApps.objects,
         function(installedApp{
                var currentApp = appsHash[installedApp.name];
                if(dependents.indexOf(currentApp) == -1 &&
                 currentApp.latest_version.dependencies[app.name]){
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
    docker = getattr(settings, 'DOCKER', None)

    def _finalize_setup():
        if docker:
            # Kill python process so docker will restart it self
            logger.error(subprocess.Popen("python /code/manage.py collectstatic --noinput && pkill -f python",
                                          shell=True, stdout=subprocess.PIPE).stdout.read())
        else:
            pass
            # working_dir = os.path.dirname(install_app_batch)
            # log_file = os.path.join(working_dir, "install_app_log.txt")
            # with open(log_file, 'a') as log:
            #     subprocess.Popen(
            #         install_app_batch,
            #         stdout=log,
            #         stderr=log,
            #         shell=True,
            #         cwd=working_dir)
            #     # stdout, stderr = p.communicate()

    timer = Timer(0.1, _finalize_setup)
    timer.start()
# TODO: add function to fix ordering in cartoview (old versions)
