# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2018 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
import logging
import os
import shutil
import sys
import time
import urllib as urllib2
import zipfile
from io import BytesIO
from urllib.request import urlopen

from paver.easy import info, needs, sh, task

try:
    from paver.path import pushd
except ImportError:
    from paver.easy import pushd

assert sys.version_info >= (2, 6), \
    SystemError("Cartoview Build requires python 2.6 or better")
TEST_DATA_URL = 'http://build.cartoview.net/cartoview_test_data.zip'
APPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps")


def grab(src, dest, name):
    download = True
    if not dest.exists():
        print('Downloading %s' % name)
    elif not zipfile.is_zipfile(dest):
        print('Downloading %s (corrupt file)' % name)
    else:
        download = False
    if download:
        if str(src).startswith("file://"):
            src2 = src[7:]
            if not os.path.exists(src2):
                print("Source location (%s) does not exist" % str(src2))
            else:
                print("Copying local file from %s" % str(src2))
                shutil.copyfile(str(src2), str(dest))
        else:
            # urllib.urlretrieve(str(src), str(dest))
            from tqdm import tqdm
            import requests
            import math
            # Streaming, so we can iterate over the response.
            r = requests.get(str(src), stream=True, timeout=10, verify=False)
            # Total size in bytes.
            total_size = int(r.headers.get('content-length', 0))
            print("Requesting %s" % str(src))
            block_size = 1024
            wrote = 0
            with open('output.bin', 'wb') as f:
                for data in tqdm(
                        r.iter_content(block_size),
                        total=math.ceil(total_size // block_size),
                        unit='KB',
                        unit_scale=False):
                    wrote = wrote + len(data)
                    f.write(data)
            print(" total_size [%d] / wrote [%d] " % (total_size, wrote))
            if total_size != 0 and wrote != total_size:
                print("ERROR, something went wrong")
            else:
                shutil.move('output.bin', str(dest))
            try:
                # Cleaning up
                os.remove('output.bin')
            except OSError:
                pass


@task
def setup_apps(options):
    from cartoview.app_manager.helpers import (create_direcotry,
                                               change_path_permission)
    try:
        f = urlopen(TEST_DATA_URL)
        zip_ref = zipfile.ZipFile(BytesIO(f.read()))
        create_direcotry(APPS_DIR)
        if not os.access(APPS_DIR, os.W_OK):
            change_path_permission(APPS_DIR)
        zip_ref.extractall(APPS_DIR)
        zip_ref.close()
    except urllib2.HTTPError as e:
        print("HTTP Error:", e.code)
    except urllib2.URLError as e:
        print("URL Error:", e.reason)


def cleanup():
    try:
        shutil.rmtree(APPS_DIR)
    except shutil.Error as e:
        logging.error(e.message)


@task
@needs([
    'setup_apps',
])
def run_cartoview_test(options):
    try:
        sh('CARTOVIEW_STAND_ALONE="True" coverage run' +
           ' --source=cartoview --omit="*/migrations/*,*/apps/*"' +
           ' ./manage.py test cartoview -v 3 ' +
           '--settings cartoview.settings')
    except Exception as e:
        cleanup()
        raise e


def _robust_rmtree(path, logger=None, max_retries=5):
    """Try to delete paths robustly .
    Retries several times (with increasing delays) if an OSError
    occurs.  If the final attempt fails, the Exception is propagated
    to the caller. Taken from https://github.com/hashdist/hashdist/pull/116
    """

    for i in range(max_retries):
        try:
            shutil.rmtree(path)
            return
        except OSError as e:
            if logger:
                info('Unable to remove path: %s' % path)
                info('Retrying after %d seconds' % i)
            time.sleep(i)

    # Final attempt, pass any Exceptions up to caller.
    shutil.rmtree(path)


@task
def run_coverage(options):
    sh(
        'CARTOVIEW_STAND_ALONE=True coverage run --source=cartoview --omit="*/migrations/*, */apps/*,pavement.py" ./manage.py test'
    )
    cleanup()


def kill(arg1, arg2):
    """Stops a proces that contains arg1 and is filtered by arg2
    """
    from subprocess import Popen, PIPE

    # Wait until ready
    t0 = time.time()
    # Wait no more than these many seconds
    time_out = 30
    running = True

    while running and time.time() - t0 < time_out:
        if os.name == 'nt':
            p = Popen(
                'tasklist | find "%s"' % arg1,
                shell=True,
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
                close_fds=False)
        else:
            p = Popen(
                'ps aux | grep %s' % arg1,
                shell=True,
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
                close_fds=True)

        lines = p.stdout.readlines()

        running = False
        for line in lines:
            # this kills all java.exe and python including self in windows
            if ('%s' % arg2 in line) or (os.name == 'nt'
                                         and '%s' % arg1 in line):
                running = True

                # Get pid
                fields = line.strip().split()

                info('Stopping %s (process number %s)' % (arg1, fields[1]))
                if os.name == 'nt':
                    kill = 'taskkill /F /PID "%s"' % fields[1]
                else:
                    kill = 'kill -9 %s 2> /dev/null' % fields[1]
                os.system(kill)

        # Give it a little more time
        time.sleep(1)
    else:
        pass

    if running:
        raise Exception('Could not stop %s: '
                        'Running processes are\n%s' % (arg1, '\n'.join(
            [l.strip() for l in lines])))


@task
@needs([
    'run_cartoview_test',
])
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
    sh("mkdocs build --config-file=./mkdocs/mkdocs.yml")
    sh("twine upload dist/*")


def _copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        elif os.path.isfile(s):
            shutil.copy2(s, d)


def justcopy(origin, target):
    if os.path.isdir(origin):
        shutil.rmtree(target, ignore_errors=True)
        _copytree(origin, target)
    elif os.path.isfile(origin):
        if not os.path.exists(target):
            os.makedirs(target)
        shutil.copy(origin, target)
