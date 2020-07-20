# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import importlib
import os
import shutil
import subprocess
import tempfile
import threading
import zipfile
from io import BytesIO
from sys import executable, exit
from threading import Timer

import pkg_resources
import requests
from django.conf import settings
from django.db import transaction
from django.db.models import Max
from future import standard_library

from cartoview.apps_handler.config import CartoviewApp
from cartoview.log_handler import get_logger
from cartoview.store_api.api import StoreAppResource, StoreAppVersion
from .decorators import restart_enabled, rollback_on_failure
from .exceptions import AppAlreadyInstalledException
from .models import App, AppStore, AppType
from ..apps_handler.req_installer import (ReqFileException,
                                          ReqFilePermissionException,
                                          ReqInstaller)

logger = get_logger(__name__)
install_app_batch = getattr(settings, 'INSTALL_APP_BAT', None)
standard_library.install_aliases()
importlib.reload(pkg_resources)

lock = threading.RLock()


class RestartHelper(object):
    @classmethod
    def django_reload(cls):
        try:
            from django.utils.autoreload import restart_with_reloader
            restart_with_reloader()
            from .utils import populate_apps
            populate_apps()
        except Exception as e:
            logger.error(e)

    @classmethod
    def restart_script(cls):
        # log_file = os.path.join(working_dir, "install_app_log.txt")
        if install_app_batch and os.path.exists(install_app_batch):
            working_dir = os.path.dirname(install_app_batch)
            # with open(log_file, 'a') as log:
            proc = subprocess.Popen(
                install_app_batch, shell=True, cwd=working_dir)
            logger.warning(proc.stdout)
            logger.error(proc.stderr)

    @classmethod
    @restart_enabled
    def restart_server(cls):
        if install_app_batch and os.path.exists(install_app_batch):
            cls.restart_script()
        else:
            cls.django_reload()
            cls.cherry_restart()

    @classmethod
    def cherry_restart(cls):
        try:
            import cherrypy
            # completely stop the cherrypy server instead of reloading
            # to avoid waiting to stop used threads error
            cherrypy.engine.stop()
            cherrypy.engine.start()
        except ImportError:
            exit(0)


def remove_unwanted(info):
    dictionary = info.__dict__.get('_data', {}) if info else {}
    app_fields = [
        str(field.name)
        for field in sorted(App._meta.fields + App._meta.many_to_many)
    ]
    app_fields.append("type")
    clean_data = {
        k: v
        for k, v in dictionary.items() if str(k) in app_fields
    }
    return clean_data


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
            category, created = AppType.objects.get_or_create(name=category)
            app.category.add(category)
        app.status = obj_property('status')
        app.tags.clear()
        app.tags.add(*obj_property('tags'))
        app.license = self.license.get('name', None) if self.license else None
        app.single_instance = obj_property('single_instance')
        return app

    def get_property_value(self, p):
        return getattr(self, p, None)


class AppInstaller(object):
    def __init__(self, name, store_id=None, version=None, user=None):
        self.user = user
        self.app_dir = os.path.join(settings.APPS_DIR, name)
        self.name = name
        self.get_store(store_id)
        self.info = None
        self.get_info()
        self.version = version
        self.get_app_version()
        self.app_serializer = AppJson(remove_unwanted(self.info))

    def get_store(self, store_id=None):
        if store_id:
            self.store = AppStore.objects.get(id=store_id)
        else:
            self.store = AppStore.objects.get(is_default=True)

    def get_app_version(self):
        if not self.version or self.version == 'latest' or \
        (self.info and self.info.latest_version.version == self.version):
            self.version = self.info.latest_version
        else:
            data = self._request_rest_data("appversion/?app__name=", self.name,
                                           "&version=", self.version)
            if "objects" in data and len(data.get("objects", [])) > 0:
                # TODO: handle if we can't get app version
                versions = data.get("objects", [])
                api_obj = StoreAppVersion()
                bundle = api_obj.build_bundle(data=versions[0])
                version = api_obj.obj_get(bundle)
                self.version = version
            else:
                self.version = None

    def get_info(self):
        data = self._request_rest_data("app/?name=", self.name)
        if "objects" in data and len(data.get("objects", [])) > 0:
            apps_list = data.get("objects", [])
            api_obj = StoreAppResource()
            for app in apps_list:
                bundle = api_obj.build_bundle(data=app)
                app_obj = api_obj.obj_get(bundle)
                self.info = app_obj
                break

    def _request_rest_data(self, *args):
        """
        get app information form app store rest url
        """
        q = requests.get(self.store.url + ''.join([str(item)
                                                   for item in args]))
        return q.json()

    @rollback_on_failure
    def extract_move_app(self, zipped_app):
        extract_to = tempfile.mkdtemp()
        libs_dir = None
        zipped_app.extractall(extract_to)
        if self.upgrade and os.path.exists(self.app_dir):
            # move old version to temporary dir so that we can restore in
            # case of failure
            old_version_temp_dir = tempfile.mkdtemp()
            shutil.move(self.app_dir, old_version_temp_dir)
            old_lib_dir = os.path.join(old_version_temp_dir, 'libs')
            if os.path.isdir(old_lib_dir) and os.path.exists(old_lib_dir):
                libs_dir = old_lib_dir
        self.new_app_dir = os.path.join(extract_to, self.name)
        shutil.move(self.new_app_dir, settings.APPS_DIR)
        if libs_dir:
            shutil.copy(libs_dir, self.app_dir)
        # delete temp extract dir
        shutil.rmtree(extract_to)

    def _download_app(self):
        response = requests.get(self.version.download_link, stream=True)
        zip_ref = zipfile.ZipFile(BytesIO(response.content))
        try:
            self.extract_move_app(zip_ref)
        except shutil.Error as e:
            logger.error(e)
            raise e
        finally:
            zip_ref.close()

    @rollback_on_failure
    def get_app_order(self):
        apps = App.objects.all()
        max_value = apps.aggregate(
            Max('order'))['order__max'] if apps.exists() else 0
        return max_value + 1

    @rollback_on_failure
    def add_carto_app(self):
        if not CartoviewApp.objects.app_exists(self.name):
            CartoviewApp({
                'name': self.name,
                'active': True,
                'order': self.get_app_order(),
                'pending': True
            })
            CartoviewApp.save()
        else:
            carto_app = CartoviewApp.objects.get(self.name)
            carto_app.pending = True
            carto_app.commit()
            CartoviewApp.save()

    @rollback_on_failure
    def add_app(self):
        # save app configuration
        app, created = App.objects.get_or_create(name=self.name)
        if created:
            if app.order is None or app.order == 0:
                app.order = self.get_app_order()
        self.add_carto_app()
        app = self.app_serializer.get_app_object(app)
        app.version = self.version.version
        app.installed_by = self.user
        app.store = AppStore.objects.filter(is_default=True).first()
        app.save()
        return app

    def _rollback(self):
        app = CartoviewApp.objects.pop(self.name, None)
        if app:
            CartoviewApp.save()
        self.delete_app_dir()

    def install(self, restart=True):
        with lock:
            self.upgrade = False
            if os.path.exists(self.app_dir):
                try:
                    installed_app = App.objects.get(name=self.name)
                    if installed_app.version < self.version.version:
                        self.upgrade = True
                    else:
                        raise AppAlreadyInstalledException()
                except App.DoesNotExist:
                    # NOTE:the following code handle if app downloaded and for
                    # some reason not added to the portal
                    self._rollback()
            installed_apps = []
            for name, version in list(self.version.dependencies.items()):
                # use try except because AppInstaller.__init__ will handle
                # upgrade if version not match
                try:
                    app_installer = AppInstaller(
                        name, self.store.id, version, user=self.user)
                    installed_apps += app_installer.install(restart=False)
                except AppAlreadyInstalledException as e:
                    logger.error(e)
            self._download_app()
            importlib.reload(pkg_resources)
            self.check_then_finlize(restart, installed_apps)
            return installed_apps

    @rollback_on_failure
    def _install_requirements(self):
        try:
            libs_dir = os.path.join(self.app_dir, 'libs')
            req_installer = ReqInstaller(self.app_dir, target=libs_dir)
            req_installer.install_all()
        except BaseException as e:
            if not (isinstance(e, ReqFileException)
                    or isinstance(e, ReqFilePermissionException)):  # noqa
                raise e

    @rollback_on_failure
    def check_then_finlize(self, restart, installed_apps):
        with transaction.atomic():
            new_app = self.add_app()
            installed_apps.append(new_app)
            self._install_requirements()
        if restart:
            timer = Timer(0.1, RestartHelper.restart_server)
            timer.start()

    def delete_app(self):
        try:
            app = App.objects.get(name=self.name)
            app.delete()
        except App.DoesNotExist:
            pass

    def delete_app_dir(self):
        if os.path.exists(self.app_dir):
            shutil.rmtree(self.app_dir)

    def completely_remove(self):
        self.delete_app()
        self.delete_app_tables()
        self.delete_app_dir()
        CartoviewApp.objects.pop(self.name, None)
        CartoviewApp.save()

    def execute_command(self, command):
        project_dir = None
        if hasattr(settings, 'BASE_DIR'):
            project_dir = settings.BASE_DIR
        elif hasattr(settings, 'PROJECT_ROOT'):
            project_dir = settings.PROJECT_ROOT
        elif hasattr(settings, 'APP_ROOT'):
            project_dir = settings.APP_ROOT
        manage_py = os.path.join(project_dir, 'manage.py')
        process = subprocess.Popen(
            "{} {} {}".format(executable, manage_py, command), shell=True)
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
                dependencies = app_installer.version.dependencies \
                    if app_installer.version else {}
                if self.name in dependencies.keys():
                    app_installer.uninstall(restart=False)
            try:
                installer = importlib.import_module('%s.installer' % self.name)
                installer.uninstall()
            except ImportError as e:
                logger.error(e)
            self.completely_remove()
            uninstalled = True
            if restart:
                RestartHelper.restart_server()
            return uninstalled
