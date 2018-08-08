import fileinput
import glob
import os
import re
import shutil
import sys
import time
import logging
import urllib2
import zipfile
from io import BytesIO

from paver.easy import (BuildFailure, call_task, cmdopts, info, needs, options,
                        path, sh, task)
from setuptools.command import easy_install

try:
    from paver.path import pushd
except ImportError:
    from paver.easy import pushd

assert sys.version_info >= (2, 6), \
    SystemError("GeoNode Build requires python 2.6 or better")
TEST_DATA_URL = 'http://build.cartoview.net/cartoview_test_data.zip'


@task
def setup_apps(options):
    from cartoview.app_manager.helpers import (
        create_direcotry, change_path_permission)
    from cartoview.settings import APPS_DIR
    try:
        f = urllib2.urlopen(TEST_DATA_URL)
        zip_ref = zipfile.ZipFile(BytesIO(f.read()))
        create_direcotry(APPS_DIR)
        if not os.access(APPS_DIR, os.W_OK):
            change_path_permission(APPS_DIR)
        zip_ref.extractall(APPS_DIR)
        zip_ref.close()
    except urllib2.HTTPError as e:
        print "HTTP Error:", e.code, url
    except urllib2.URLError as e:
        print "URL Error:", e.reason, url


def cleanup():
    from cartoview.settings import APPS_DIR
    try:
        shutil.rmtree(APPS_DIR)
    except shutil.Error as e:
        logging.error(e.message)


@task
@needs(['setup_apps', ])
def run_test(options):
    try:
        sh('CARTOVIEW_STAND_ALONE=True python manage.py test cartoview --with-coverage --cover-package=cartoview -v 2')
    except Exception as e:
        cleanup()
        raise e


@task
def run_coverage(options):
    sh('CARTOVIEW_STAND_ALONE=True coverage run --source=cartoview --omit="*/migrations/*, */apps/*,pavement.py" ./manage.py test')
    cleanup()


@task
@needs(['run_test', ])
def publish(options):
    from cartoview.settings import BASE_DIR
    dist_dir = os.path.join(BASE_DIR, 'dist')
    build_dir = os.path.join(BASE_DIR, 'build')
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    sh("pip install twine")
    sh("python setup.py sdist")
    sh("python setup.py bdist_wheel")
    sh("twine upload dist/*")
