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
import json
import logging
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib
import urllib as urllib2
import zipfile
from io import BytesIO
import datetime
from urllib.parse import urlparse
from urllib.request import urlopen, Request
import requests
import math
import psutil
import pytz
from dateutil.parser import parse as parsedate
from tqdm import tqdm

from cartoview.settings import (
    on_travis,
    INSTALLED_APPS,
    OGC_SERVER
)

import yaml
from paver.easy import cmdopts, info, needs, path, sh, task

try:
    from paver.path import pushd
except ImportError:
    from paver.easy import pushd

assert sys.version_info >= (2, 6), \
    SystemError("Cartoview Build requires python 2.6 or better")
TEST_DATA_URL = 'http://build.cartoview.net/cartoview_test_data.zip'
dev_config = None
with open("dev_config.yml") as f:
    dev_config = yaml.load(f, Loader=yaml.Loader)
APPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps")

logger = logging.getLogger(__name__)


def grab(src, dest, name):
    src, dest, name = map(str, (src, dest, name))
    logger.info(f" src, dest, name --> {src} {dest} {name}")

    if not os.path.exists(dest):
        logger.info(f"Downloading {name}")
    elif not zipfile.is_zipfile(dest):
        logger.info(f"Downloading {name} (corrupt file)")
    elif not src.startswith("file://"):
        r = requests.head(src)
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(dest))
        url_time = file_time
        for _k in ['last-modified', 'Date']:
            if _k in r.headers:
                url_time = r.headers[_k]
        url_date = parsedate(url_time)
        utc = pytz.utc
        url_date = url_date.replace(tzinfo=utc)
        file_time = file_time.replace(tzinfo=utc)
        if url_date < file_time:
            # Do not download if older than the local one
            return
        logger.info(f"Downloading updated {name}")

    # Local file does not exist or remote one is newer
    if src.startswith("file://"):
        src2 = src.replace("file://", '')
        if not os.path.exists(src2):
            logger.info(f"Source location ({src2}) does not exist")
        else:
            logger.info(f"Copying local file from {src2}")
            shutil.copyfile(src2, dest)
    else:
        # urlretrieve(str(src), str(dest))
        # Streaming, so we can iterate over the response.
        r = requests.get(src, stream=True, timeout=10, verify=False)
        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0))
        logger.info(f"Requesting {src}")
        block_size = 1024
        wrote = 0
        with open("output.bin", 'wb') as f:
            for data in tqdm(
                    r.iter_content(block_size),
                    total=math.ceil(total_size // block_size),
                    unit='KB',
                    unit_scale=False):
                wrote += len(data)
                f.write(data)
        logger.info(f" total_size [{total_size}] / wrote [{wrote}] ")
        if total_size != 0 and wrote != total_size:
            logger.error(
                f"ERROR, something went wrong. Data could not be written. Expected to write {wrote} but wrote {total_size} instead")
        else:
            shutil.move("output.bin", dest)
        try:
            # Cleaning up
            os.remove("output.bin")
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
        sh('coverage run' +
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


def _install_data_dir():
    target_data_dir = path('geoserver/data')
    if target_data_dir.exists():
        try:
            target_data_dir.rmtree()
        except OSError:
            _robust_rmtree(target_data_dir, logger=True)

    original_data_dir = path('geoserver/geoserver/data')
    justcopy(original_data_dir, target_data_dir)

    try:
        config = path('geoserver/data/global.xml')
        with open(config) as f:
            xml = f.read()
            m = re.search('proxyBaseUrl>([^<]+)', xml)
            xml = xml[:m.start(1)] + \
                  "http://localhost:8080/geoserver" + xml[m.end(1):]
            with open(config, 'w') as f:
                f.write(xml)
    except Exception as e:
        print(e)

    try:
        config = path(
            'geoserver/data/security/filter/geonode-oauth2/config.xml')
        with open(config) as f:
            xml = f.read()
            m = re.search('accessTokenUri>([^<]+)', xml)
            xml = xml[:m.start(1)] + \
                  "http://localhost:8000/o/token/" + xml[m.end(1):]
            m = re.search('userAuthorizationUri>([^<]+)', xml)
            xml = xml[:m.start(
                1)] + "http://localhost:8000/o/authorize/" + xml[m.end(1):]
            m = re.search('redirectUri>([^<]+)', xml)
            xml = xml[:m.start(
                1
            )] + "http://localhost:8080/geoserver/index.html" + xml[m.end(1):]
            m = re.search('checkTokenEndpointUrl>([^<]+)', xml)
            xml = xml[:m.start(
                1
            )] + "http://localhost:8000/api/o/v4/tokeninfo/" + xml[m.end(1):]
            m = re.search('logoutUri>([^<]+)', xml)
            xml = xml[:m.start(
                1)] + "http://localhost:8000/account/logout/" + xml[m.end(1):]
            with open(config, 'w') as f:
                f.write(xml)
    except Exception as e:
        print(e)

    try:
        config = path(
            'geoserver/data/security/role/geonode REST role service/config.xml'
        )
        with open(config) as f:
            xml = f.read()
            m = re.search('baseUrl>([^<]+)', xml)
            xml = xml[:m.start(1)] + "http://localhost:8000" + xml[m.end(1):]
            with open(config, 'w') as f:
                f.write(xml)
    except Exception as e:
        print(e)


@task
@cmdopts([
    ('geoserver=', 'g', 'The location of the geoserver build (.war file).'),
    ('jetty=', 'j', 'The location of the Jetty Runner (.jar file).'),
    ('force_exec=', '', 'Force GeoServer Setup.')
])
def setup_geoserver(options):
    """Prepare a testing instance of GeoServer."""
    # only start if using Geoserver backend
    if 'geonode.geoserver' not in INSTALLED_APPS:
        return
    if on_travis and not options.get('force_exec', False):
        """Will make use of the docker container for the Integration Tests"""
        return
    else:
        download_dir = path('downloaded')
        if not download_dir.exists():
            download_dir.makedirs()
        geoserver_dir = path('geoserver')
        geoserver_bin = download_dir / \
                        os.path.basename(urlparse(dev_config['GEOSERVER_URL']).path)
        jetty_runner = download_dir / \
                       os.path.basename(urlparse(dev_config['JETTY_RUNNER_URL']).path)
        geoserver_data = download_dir / \
                         os.path.basename(urlparse(dev_config['DATA_DIR_URL']).path)
        grab(
            options.get(
                'geoserver',
                dev_config['GEOSERVER_URL']),
            geoserver_bin,
            "geoserver binary")
        grab(
            options.get(
                'jetty',
                dev_config['JETTY_RUNNER_URL']),
            jetty_runner,
            "jetty runner")
        grab(
            options.get(
                'geoserver data',
                dev_config['DATA_DIR_URL']),
            geoserver_data,
            "geoserver data-dir")

        if not geoserver_dir.exists():
            geoserver_dir.makedirs()

            webapp_dir = geoserver_dir / 'geoserver'
            if not webapp_dir:
                webapp_dir.makedirs()

            logger.info("extracting geoserver")
            z = zipfile.ZipFile(geoserver_bin, "r")
            z.extractall(webapp_dir)

            logger.info("extracting geoserver data dir")
            z = zipfile.ZipFile(geoserver_data, "r")
            z.extractall(geoserver_dir)

        _configure_data_dir()


def _configure_data_dir():
    try:
        config = path(
            'geoserver/data/global.xml')
        with open(config) as f:
            xml = f.read()
            m = re.search('proxyBaseUrl>([^<]+)', xml)
            xml = f"{xml[:m.start(1)]}http://localhost:8080/geoserver{xml[m.end(1):]}"
            with open(config, 'w') as f:
                f.write(xml)
    except Exception as e:
        print(e)

    try:
        config = path(
            'geoserver/data/security/filter/geonode-oauth2/config.xml')
        with open(config) as f:
            xml = f.read()
            m = re.search('accessTokenUri>([^<]+)', xml)
            xml = f"{xml[:m.start(1)]}http://localhost:8000/o/token/{xml[m.end(1):]}"
            m = re.search('userAuthorizationUri>([^<]+)', xml)
            xml = f"{xml[:m.start(1)]}http://localhost:8000/o/authorize/{xml[m.end(1):]}"
            m = re.search('redirectUri>([^<]+)', xml)
            xml = f"{xml[:m.start(1)]}http://localhost:8080/geoserver/index.html{xml[m.end(1):]}"
            m = re.search('checkTokenEndpointUrl>([^<]+)', xml)
            xml = f"{xml[:m.start(1)]}http://localhost:8000/api/o/v4/tokeninfo/{xml[m.end(1):]}"
            m = re.search('logoutUri>([^<]+)', xml)
            xml = f"{xml[:m.start(1)]}http://localhost:8000/account/logout/{xml[m.end(1):]}"
            with open(config, 'w') as f:
                f.write(xml)
    except Exception as e:
        print(e)

    try:
        config = path(
            'geoserver/data/security/role/geonode REST role service/config.xml')
        with open(config) as f:
            xml = f.read()
            m = re.search('baseUrl>([^<]+)', xml)
            xml = f"{xml[:m.start(1)]}http://localhost:8000{xml[m.end(1):]}"
            with open(config, 'w') as f:
                f.write(xml)
    except Exception as e:
        print(e)


@task
@cmdopts([
    ('java_path=', 'j', 'Full path to java install for Windows'),
    ('force_exec=', '', 'Force GeoServer Start.')
])
def start_geoserver(options):
    """
    Start GeoServer with GeoNode extensions
    """
    # we use docker-compose for integration tests
    if on_travis and not options.get('force_exec', False):
        return

    # only start if using Geoserver backend
    if 'geonode.geoserver' not in INSTALLED_APPS:
        return

    GEOSERVER_BASE_URL = OGC_SERVER['default']['LOCATION']
    url = GEOSERVER_BASE_URL

    if urlparse(GEOSERVER_BASE_URL).hostname != 'localhost':
        logger.warning("Warning: OGC_SERVER['default']['LOCATION'] hostname is not equal to 'localhost'")

    if not GEOSERVER_BASE_URL.endswith('/'):
        logger.error("Error: OGC_SERVER['default']['LOCATION'] does not end with a '/'")
        sys.exit(1)

    download_dir = path('downloaded').abspath()
    jetty_runner = download_dir / \
                   os.path.basename(dev_config['JETTY_RUNNER_URL'])
    data_dir = path('geoserver/data').abspath()
    geofence_dir = path('geoserver/data/geofence').abspath()
    web_app = path('geoserver/geoserver').abspath()
    log_file = path('geoserver/jetty.log').abspath()
    config = path('scripts/misc/jetty-runner.xml').abspath()
    jetty_port = urlparse(GEOSERVER_BASE_URL).port

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_free = True
    try:
        s.bind(("127.0.0.1", jetty_port))
    except OSError as e:
        socket_free = False
        if e.errno == 98:
            info(f'Port {jetty_port} is already in use')
        else:
            info(
                f'Something else raised the socket.error exception while checking port {jetty_port}')
            print(e)
    finally:
        s.close()

    if socket_free:
        # @todo - we should not have set workdir to the datadir but a bug in geoserver
        # prevents geonode security from initializing correctly otherwise
        with pushd(data_dir):
            javapath = "java"
            if on_travis:
                sh(
                    'sudo apt install -y openjdk-8-jre openjdk-8-jdk;'
                    ' sudo update-java-alternatives --set java-1.8.0-openjdk-amd64;'
                    ' export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::");'
                    ' export PATH=$JAVA_HOME\'bin/java\':$PATH;'
                )
                # import subprocess
                # result = subprocess.run(['update-alternatives', '--list', 'java'], stdout=subprocess.PIPE)
                # javapath = result.stdout
                javapath = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"
            loggernullpath = os.devnull

            # checking if our loggernullpath exists and if not, reset it to
            # something manageable
            if loggernullpath == "nul":
                try:
                    open("../../downloaded/null.txt", 'w+').close()
                except OSError:
                    print("Chances are that you have Geoserver currently running. You "
                          "can either stop all servers with paver stop or start only "
                          "the django application with paver start_django.")
                    sys.exit(1)
                loggernullpath = "../../downloaded/null.txt"

            try:
                sh('%(javapath)s -version' % locals())
            except Exception:
                logger.warning("Java was not found in your path.  Trying some other options: ")
                javapath_opt = None
                if os.environ.get('JAVA_HOME', None):
                    logger.info("Using the JAVA_HOME environment variable")
                    javapath_opt = os.path.join(os.path.abspath(
                        os.environ['JAVA_HOME']), "bin", "java.exe")
                elif options.get('java_path'):
                    javapath_opt = options.get('java_path')
                else:
                    logger.critical("Paver cannot find java in the Windows Environment. "
                                    "Please provide the --java_path flag with your full path to "
                                    "java.exe e.g. --java_path=C:/path/to/java/bin/java.exe")
                    sys.exit(1)
                # if there are spaces
                javapath = f"START /B \"\" \"{javapath_opt}\""

            sh(
                '%(javapath)s -Xms512m -Xmx2048m -server -XX:+UseConcMarkSweepGC -XX:MaxPermSize=512m'
                ' -DGEOSERVER_DATA_DIR=%(data_dir)s'
                ' -DGEOSERVER_CSRF_DISABLED=true'
                ' -Dgeofence.dir=%(geofence_dir)s'
                ' -Djava.awt.headless=true'
                # ' -Dgeofence-ovr=geofence-datasource-ovr.properties'
                # workaround for JAI sealed jar issue and jetty classloader
                # ' -Dorg.eclipse.jetty.server.webapp.parentLoaderPriority=true'
                ' -jar %(jetty_runner)s'
                ' --port %(jetty_port)i'
                ' --log %(log_file)s'
                ' %(config)s'
                ' > %(loggernullpath)s &' % locals()
            )

        info(f'Starting GeoServer on {url}')

    # wait for GeoServer to start
    started = waitfor(url)
    info(f'The logs are available at {log_file}')

    if not started:
        # If applications did not start in time we will give the user a chance
        # to inspect them and stop them manually.
        info('GeoServer never started properly or timed out.'
             'It may still be running in the background.')
        sys.exit(1)


def waitfor(url, timeout=300):
    started = False
    for a in range(timeout):
        try:
            resp = urlopen(url)
        except IOError:
            pass
        else:
            if resp.getcode() == 200:
                started = True
                break
        time.sleep(1)
    return started


@task
def run_coverage(options):
    sh(
        'coverage run --source=cartoview --omit="*/migrations/*, */apps/*,pavement.py" ./manage.py test'
    )
    cleanup()


def kill(arg1, arg2):
    """
    Stops a proces that contains arg1 and is filtered by arg2
    """
    from subprocess import Popen, PIPE

    # Wait until ready
    t0 = time.time()
    # Wait no more than these many seconds
    time_out = 30
    running = True

    while running and time.time() - t0 < time_out:
        if os.name == 'nt':
            p = Popen(f'tasklist | find "{arg1}"', shell=True,
                      stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=False)
        else:
            p = Popen(f'ps aux | grep {arg1}', shell=True,
                      stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

        lines = p.stdout.readlines()

        running = False
        for line in lines:
            # this kills all java.exe and python including self in windows
            if (f'{arg2}' in str(line)) or (os.name == 'nt' and f'{arg1}' in str(line)):
                running = True

                # Get pid
                fields = line.strip().split()

                info(f'Stopping {arg1} (process number {int(fields[1])})')
                if os.name == 'nt':
                    kill = f'taskkill /F /PID "{int(fields[1])}"'
                else:
                    kill = f'kill -9 {int(fields[1])} 2> /dev/null'
                os.system(kill)

        # Give it a little more time
        time.sleep(1)

    if running:
        _procs = '\n'.join([str(_l).strip() for _l in lines])
        raise Exception(f"Could not stop {arg1}: "
                        f"Running processes are\n{_procs}")


@task
@cmdopts([
    ('force_exec=', '', 'Force GeoServer Stop.')
])
def stop_geoserver(options):
    """
        Stop GeoServer
        """
    # we use docker-compose for integration tests
    if on_travis and not options.get('force_exec', False):
        return

    # only start if using Geoserver backend
    if 'geonode.geoserver' not in INSTALLED_APPS:
        return
    kill('java', 'geoserver')

    # Kill process.
    try:
        # proc = subprocess.Popen("ps -ef | grep -i -e '[j]ava\|geoserver' |
        # awk '{print $2}'",
        proc = subprocess.Popen(
            "ps -ef | grep -i -e 'geoserver' | awk '{print $2}'",
            shell=True,
            stdout=subprocess.PIPE)
        for pid in map(int, proc.stdout):
            info(f'Stopping geoserver (process number {pid})')
            os.kill(pid, signal.SIGKILL)

            # Check if the process that we killed is alive.
            killed, alive = psutil.wait_procs([psutil.Process(pid=pid)], timeout=30)
            for p in alive:
                p.kill()
    except Exception as e:
        info(e)


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


@task
def install_docker_data_dir():
    siteurl = os.environ.get('SITEURL', 'http://localhost/')
    nginx_location = os.environ.get("NGINX_LOCATION", "http://nginx:80/")

    geoserver_data_dir = path('/geoserver_data/data')
    global_conf = os.path.join(geoserver_data_dir, 'global.xml')
    security_filter_conf = os.path.join(geoserver_data_dir, path('security/filter/geonode-oauth2/config.xml'))
    security_role_conf = os.path.join(geoserver_data_dir, path('security/role/geonode REST role service/config.xml'))

    try:
        config = global_conf
        with open(config) as f:
            xml = f.read()
            m = re.search('proxyBaseUrl>([^<]+)', xml)
            xml = xml[:m.start(1)] + \
                  "{}geoserver".format(siteurl) + xml[m.end(1):]
            with open(config, 'w') as f:
                f.write(xml)
    except Exception as e:
        print('Error while modifying {} :'.format(security_role_conf), e)

    try:
        config = security_filter_conf
        with open(config) as f:
            xml = f.read()
            m = re.search('accessTokenUri>([^<]+)', xml)
            xml = xml[:m.start(1)] + \
                  "{}o/token/".format(nginx_location) + xml[m.end(1):]
            m = re.search('userAuthorizationUri>([^<]+)', xml)
            xml = xml[:m.start(
                1)] + "{}o/authorize/".format(siteurl) + xml[m.end(1):]
            m = re.search('redirectUri>([^<]+)', xml)
            xml = xml[:m.start(
                1)] + "{}geoserver/index.html".format(siteurl) + xml[m.end(1):]
            m = re.search('checkTokenEndpointUrl>([^<]+)', xml)
            xml = xml[:m.start(
                1)] + "{}api/o/v4/tokeninfo/".format(nginx_location) + xml[m.end(1):]
            m = re.search('logoutUri>([^<]+)', xml)
            xml = xml[:m.start(
                1)] + "{}account/logout/".format(siteurl) + xml[m.end(1):]
            with open(config, 'w') as f:
                f.write(xml)
    except Exception as e:
        print('Error while modifying {} :'.format(security_filter_conf), e)

    try:
        config = security_role_conf
        with open(config) as f:
            xml = f.read()
            m = re.search('baseUrl>([^<]+)', xml)
            xml = xml[:m.start(1)] + nginx_location[:-1] + xml[m.end(1):]
            with open(config, 'w') as f:
                f.write(xml)
    except Exception as e:
        print('Error while modifying {} :'.format(security_role_conf), e)


@task
def prepare_docker_oauth_fixture():
    project_name = os.environ.get('PROJECT_NAME', 'cartoview')
    fixturefile = path('{}/fixtures/default_oauth_apps_docker.json'.format(project_name))
    os.remove(fixturefile)
    siteurl = os.environ.get('SITEURL', 'http://localhost/')
    default_fixture = [
        {
            "model": "oauth2_provider.application",
            "pk": 1001,
            "fields": {
                "skip_authorization": True,
                "created": "2018-05-31T10:00:31.661Z",
                "updated": "2018-05-31T11:30:31.245Z",
                "algorithm": "RS256",
                "redirect_uris": "{}geoserver/index.html".format(siteurl),
                "name": "GeoServer",
                "authorization_grant_type": "authorization-code",
                "client_type": "confidential",
                "client_id": "Jrchz2oPY3akmzndmgUTYrs9gczlgoV20YPSvqaV",
                "client_secret": "\
rCnp5txobUo83EpQEblM8fVj3QT5zb5qRfxNsuPzCqZaiRyIoxM4jdgMiZKFfePBHYXCLd7B8NlkfDB\
Y9HKeIQPcy5Cp08KQNpRHQbjpLItDHv12GvkSeXp6OxaUETv3",
                "user": [
                    "admin"
                ]
            }
        }
    ]
    with open(fixturefile, 'w') as ff:
        json.dump(default_fixture, ff)
