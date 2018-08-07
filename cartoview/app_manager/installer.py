# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import zipfile
from builtins import *
from io import BytesIO
from sys import executable, exit
from threading import Timer

import pkg_resources
import portalocker
import requests
import yaml
from django.conf import settings
from django.db import transaction
from django.db.models import Max
from future import standard_library

from cartoview.log_handler import get_logger

from .config import App as AppConfig
from .helpers import change_path_permission, create_direcotry
from .models import App, AppStore, AppType
from .settings import create_apps_dir

logger = get_logger(__name__)
install_app_batch = getattr(settings, 'INSTALL_APP_BAT', None)
standard_library.install_aliases()
reload(pkg_resources)
current_folder = os.path.abspath(os.path.dirname(__file__))
temp_dir = os.path.join(current_folder, 'temp')

lock = threading.RLock()


class FinalizeInstaller:
    def __init__(self):
        self.apps_to_finlize = []

    def save_pending_app_to_finlize(self):
        with open(settings.PENDING_APPS, 'wb') as outfile:
            portalocker.lock(outfile, portalocker.LOCK_EX)
            yaml.dump(self.apps_to_finlize, outfile, default_flow_style=False)
        self.apps_to_finlize = []

    def restart_server(self):
        # log_file = os.path.join(working_dir, "install_app_log.txt")
        if install_app_batch and os.path.exists(install_app_batch):
            working_dir = os.path.dirname(install_app_batch)
            # with open(log_file, 'a') as log:
            proc = subprocess.Popen(
                install_app_batch,
                shell=True,
                cwd=working_dir)
            logger.warning(proc.stdout)
            logger.error(proc.stderr)

    def docker_restart(self):
        try:
            import cherrypy
            cherrypy.engine.restart()
        except ImportError:
            exit(0)

    def finalize_setup(self, app_name):
        self.save_pending_app_to_finlize()
        docker = getattr(settings, 'DOCKER', None)

        def _finalize_setup(app_name):
            if docker:
                self.docker_restart()
            else:
                self.restart_server()
        if 'test' not in sys.argv:
            timer = Timer(0.1, _finalize_setup(app_name))
            timer.start()

    def __call__(self, app_name):
        self.finalize_setup(app_name)


FINALIZE_SETUP = FinalizeInstaller()


def remove_unwanted(dictionary):
    app_fields = [field.name for field in
                  sorted(App._meta.fields + App._meta.many_to_many)]
    app_fields.append("type")
    return {k: v for k, v in dictionary.iteritems() if k in app_fields}


class AppJson(object):
    def __init__(self, dictionary):
        self.__dict__ = dictionary

    def get_app_object(self, app):
        obj_property = self.get_property_value
        app.title = self.title
        app.description = self.description
        # TODO:remove short_description
        app.short_description = self.description
        app.owner_url = obj_property('owner_url')
        app.help_url = obj_property('help_url')
        app.author = obj_property('author')
        app.author_website = obj_property('author_website')
        app.home_page = obj_property('demo_url')
        for category in self.type:
            category, created = AppType.objects.get_or_create(
                name=category)
            app.category.add(category)
        app.status = obj_property('status')
        app.tags.clear()
        app.tags.add(*obj_property('tags'))
        app.license = self.license.get(
            'name', None) if self.license else None
        app.single_instance = obj_property('single_instance')
        return app

    def get_property_value(self, p):
        return getattr(self, p, None)


class AppAlreadyInstalledException(BaseException):
    message = "Application is already installed."


class AppInstaller(object):

    def __init__(self, name, store_id=None, version=None, user=None):
        create_apps_dir()
        self.user = user
        self.app_dir = os.path.join(settings.APPS_DIR, name)
        self.name = name
        if store_id is None:
            self.store = AppStore.objects.get(is_default=True)
        else:
            self.store = AppStore.objects.get(id=store_id)
        self.info = self._request_rest_data("app/?name=", name)['objects'][0]
        self.version = version
        self.get_app_version()
        self.app_serializer = AppJson(remove_unwanted(self.info))

    def get_app_version(self):
        if self.version is None or self.version == 'latest' or self.info[
                "latest_version"]["version"] == self.version:
            self.version = self.info["latest_version"]
        else:
            data = self._request_rest_data("appversion/?app__name=", name,
                                           "&version=", self.version)
            self.version = data['objects'][0]

    def _request_rest_data(self, *args):
        """
        get app information form app store rest url
        """
        q = requests.get(self.store.url + ''.join(
            [str(item) for item in args]))
        return q.json()

    def extract_move_app(self, zipped_app):
        extract_to = tempfile.mkdtemp(dir=temp_dir)
        zipped_app.extractall(extract_to)
        if self.upgrade and os.path.exists(self.app_dir):
            # move old version to temporary dir so that we can restore in
            # case of failure
            old_version_temp_dir = tempfile.mkdtemp(dir=temp_dir)
            shutil.move(self.app_dir, old_version_temp_dir)
        self.old_app_temp_dir = os.path.join(extract_to, self.name)
        shutil.move(self.old_app_temp_dir, settings.APPS_DIR)
        # delete temp extract dir
        shutil.rmtree(extract_to)

    def _download_app(self):
        # TODO: improve download apps (server-side)
        response = requests.get(self.version["download_link"], stream=True)
        zip_ref = zipfile.ZipFile(
            BytesIO(response.content))
        try:
            create_direcotry(temp_dir)
            if not os.access(temp_dir, os.W_OK):
                change_path_permission(temp_dir)
            self.extract_move_app(zip_ref)
        except shutil.Error as e:
            logger.error(e.message)
            raise e
        finally:
            zip_ref.close()

    def get_app_order(self):
        apps = App.objects.all()
        max_value = apps.aggregate(
            Max('order'))['order__max'] if apps.exists() else 0
        return max_value+1

    def add_app(self, installer):
        # save app configuration
        app, created = App.objects.get_or_create(name=self.name)
        if created:
            # append app in order
            if app.order is None or app.order == 0:
                app.order = self.get_app_order()
            app_config = AppConfig(
                name=self.name, active=True, order=app.order)
            app.apps_config.append(app_config)
            app.apps_config.save()
        app = self.app_serializer.get_app_object(app)
        app.version = self.version["version"]
        app.installed_by = self.user
        app.store = AppStore.objects.filter(is_default=True).first()
        app.save()
        return app

    def _rollback(self):
        from django.conf import settings
        apps_file_path = os.path.join(settings.APPS_DIR, "apps.yml")
        apps_config = AppsConfig(apps_file_path)
        shutil.rmtree(self.app_dir)
        apps_config = AppConfig(apps_file_path)
        app_conf = apps_config.get_by_name(self.name)
        if app_conf:
            del app_conf

    def install(self, restart=True):
        with lock:
            self.upgrade = False
            if os.path.exists(self.app_dir):
                try:
                    installed_app = App.objects.get(name=self.name)
                    if installed_app.version < self.version["version"]:
                        self.upgrade = True
                    else:
                        raise AppAlreadyInstalledException()
                except App.DoesNotExist:
                    # NOTE:the following code handle if app downloaded and for some reason not added to the portal
                    self._rollback()
            installed_apps = []
            for name, version in list(self.version["dependencies"].items()):
                # use try except because AppInstaller.__init__ will handle upgrade
                # if version not match
                try:
                    app_installer = AppInstaller(
                        name, self.store.id, version, user=self.user)
                    installed_apps += app_installer.install(restart=False)
                except AppAlreadyInstalledException as e:
                    logger.error(e.message)
            self._download_app()
            reload(pkg_resources)
            self.check_then_finlize(restart, installed_apps)
            return installed_apps

    @transaction.atomic
    def check_then_finlize(self, restart, installed_apps):
        try:
            installer = importlib.import_module('%s.installer' % self.name)
            new_app = self.add_app(installer)
            installed_apps.append(new_app)
            try:
                installer.install()
            except Exception as e:
                logger.error(e.message)
            FINALIZE_SETUP.apps_to_finlize.append(self.name)
            if restart:
                FINALIZE_SETUP(self.name)
        except ImportError as ex:
            logger.error(ex.message)
            if os.path.exists(self.app_dir):
                self._rollback()
                raise ex

    def completely_remove(self):
        app = App.objects.get(name=self.name)
        app_config = app.apps_config.get_by_name(self.name)
        del app.apps_config[app_config]
        app.apps_config.save()
        app.delete()

    def execute_command(self, command):
        manage_py = os.path.join(settings.BASE_DIR, 'manage.py')
        process = subprocess.Popen("{} {} {}".format(
            executable, manage_py, command), shell=True)
        out, err = process.communicate()
        logger.info(out)
        logger.error(err)

    def delete_app_tables(self):
        from django.contrib.contenttypes.models import ContentType
        ContentType.objects.filter(app_label=self.name).delete()
        self.execute_command("migrate {} zero".format(self.name))

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
        with lock:
            uninstalled = False
            installed_apps = App.objects.all()
            for app in installed_apps:
                app_installer = AppInstaller(
                    app.name, self.store.id, app.version, user=self.user)
                dependencies = app_installer.version["dependencies"]
                if self.name in dependencies:
                    app_installer.uninstall(restart=False)
            installer = importlib.import_module('%s.installer' % self.name)
            installer.uninstall()
            self.delete_app_tables()
            self.completely_remove()
            app_dir = os.path.join(settings.APPS_DIR, self.name)
            shutil.rmtree(app_dir)
            uninstalled = True
            if restart:
                FINALIZE_SETUP.restart_server()
            return uninstalled
