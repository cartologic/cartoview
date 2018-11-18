# -*- coding: utf-8 -*-
from __future__ import print_function
import ast
import copy
import os
import re
import sys
from distutils.util import strtobool

import dj_database_url
from geonode.settings import *  # noqa
from kombu import Exchange, Queue

import cartoview

CARTOVIEW_INSTALLED_APPS = ("cartoview",
                            "cartoview.cartoview_api.apps.CartoviewAPIConfig",
                            "cartoview.store_api.apps.StoreApiConfig",
                            "cartoview.app_manager",
                            "cartoview.site_management",
                            "cartoview.apps_handler.apps.AppsHandlerConfig")
INSTALLED_APPS += CARTOVIEW_INSTALLED_APPS
ROOT_URLCONF = "cartoview.urls"
CARTOVIEW_DIR = os.path.abspath(os.path.dirname(cartoview.__file__))
BASE_DIR = os.path.dirname(CARTOVIEW_DIR)
CARTOVIEW_TEMPLATE_DIRS = [
    os.path.join(CARTOVIEW_DIR, "templates"),
]
# TEMPLATES[0]["DIRS"] = CARTOVIEW_TEMPLATE_DIRS
CARTOVIEW_STATIC_DIRS = [
    os.path.join(CARTOVIEW_DIR, "static"),
]
STATICFILES_DIRS += CARTOVIEW_STATIC_DIRS
APPS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(CARTOVIEW_DIR), "apps"))
PENDING_APPS = os.path.join(APPS_DIR, "pendingOperation.yml")
APPS_MENU = False
DOCKER = os.getenv('DOCKER', False)
CARTOVIEW_CONTEXT_PROCESSORS = (
    'cartoview.app_manager.context_processors.cartoview_processor',
    'cartoview.app_manager.context_processors.site_logo')
TEMPLATES[0]["OPTIONS"]['context_processors'] += CARTOVIEW_CONTEXT_PROCESSORS
# django Media Section
# uncomment the following if you want your files out of geonode folder
MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded")
MEDIA_URL = "/uploaded/"
LOCAL_MEDIA_URL = "/uploaded/"
# static section
STATIC_ROOT = os.path.join(BASE_DIR, "static")
DATABASE_URL = os.getenv(
    'DATABASE_URL', 'sqlite:////{}/database.sqlite'.format(
        os.path.dirname(CARTOVIEW_DIR)))
DATASTORE_DATABASE_URL = os.getenv('DATASTORE_DATABASE_URL', None)
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(
        DATABASE_URL, conn_max_age=600)
if DATASTORE_DATABASE_URL:
    DATABASES['datastore'] = dj_database_url.parse(
        DATASTORE_DATABASE_URL, conn_max_age=600)
try:
    # try to parse python notation, default in dockerized env
    ALLOWED_HOSTS = ast.literal_eval(os.getenv('ALLOWED_HOSTS'))
except ValueError:
    # fallback to regular list of values separated with misc chars
    ALLOWED_HOSTS = ['*'] if os.getenv('ALLOWED_HOSTS') is None \
        else re.split(r' *[,|:|;] *', os.getenv('ALLOWED_HOSTS'))
try:
    from .local_settings import *
except Exception as e:
    pass

CARTOVIEW_TEST = 'test' in sys.argv or ast.literal_eval(
    os.getenv('CARTOVIEW_TEST', "False")) or 'run_cartoview_test' in sys.argv

if CARTOVIEW_TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'test.db')
        }
    }
if 'datastore' in DATABASES:
    OGC_SERVER['default']['DATASTORE'] = 'datastore'

if 'geonode.geoserver' in INSTALLED_APPS and "LOCAL_GEOSERVER" in \
        locals() and LOCAL_GEOSERVER in MAP_BASELAYERS:
    LOCAL_GEOSERVER["source"][
        "url"] = OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms"

# Logging settings
# 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'
DJANGO_LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'ERROR')

installed_apps_conf = {
    'handlers': ['console'],
    'level': DJANGO_LOG_LEVEL,
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            ('%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d'
             ' %(message)s'),
        },
    },
    'handlers': {
        'console': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers':
    {app: copy.deepcopy(installed_apps_conf)
     for app in INSTALLED_APPS},
    'root': {
        'handlers': ['console'],
        'level': DJANGO_LOG_LEVEL
    },
}

LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['console'],
    'propagate': False,
    'level': 'WARNING',  # Django SQL logging is too noisy at DEBUG
}

# NOTE:set cartoview_stand_alone environment var if you are not using
# cartoview_proect_template
CARTOVIEW_STAND_ALONE = strtobool(os.getenv('CARTOVIEW_STAND_ALONE', 'FALSE'))
if CARTOVIEW_STAND_ALONE or CARTOVIEW_TEST:
    TEMPLATES[0]["DIRS"] = CARTOVIEW_TEMPLATE_DIRS + TEMPLATES[0]["DIRS"]
    from cartoview import app_manager
    from past.builtins import execfile
    app_manager_settings = os.path.join(
        os.path.dirname(app_manager.__file__), "settings.py")
    execfile(os.path.realpath(app_manager_settings))
    load_apps(APPS_DIR)
    INSTALLED_APPS += CARTOVIEW_APPS
    for settings_file in APPS_SETTINGS:
        try:
            execfile(settings_file)
        except Exception as e:
            print(e.message)

# Celery settings
CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_DEFAULT_EXCHANGE = "default"
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_TASK_DEFAULT_ROUTING_KEY = "default"
# Celery settings
ASYNC_SIGNALS = ast.literal_eval(os.environ.get('ASYNC_SIGNALS', 'False'))
RABBITMQ_SIGNALS_BROKER_URL = 'amqp://rabbitmq:5672'
REDIS_SIGNALS_BROKER_URL = 'redis://redis:6379/0'
LOCAL_SIGNALS_BROKER_URL = 'memory://'

if ASYNC_SIGNALS:
    _BROKER_URL = os.environ.get('BROKER_URL', RABBITMQ_SIGNALS_BROKER_URL)
    # _BROKER_URL =  = os.environ.get('BROKER_URL', REDIS_SIGNALS_BROKER_URL)
    CELERY_RESULT_BACKEND = _BROKER_URL
    CELERY_RESULT_BACKEND = "rpc" + _BROKER_URL[4:]
else:
    _BROKER_URL = LOCAL_SIGNALS_BROKER_URL

BROKER_URL = _BROKER_URL
CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_PERSISTENT = False

# Allow to recover from any unknown crash.
CELERY_ACKS_LATE = True

# Set this to False in order to run async
CELERY_TASK_ALWAYS_EAGER = False if ASYNC_SIGNALS else True
CELERY_ALWAYS_EAGER = False if ASYNC_SIGNALS else True
CELERY_TASK_IGNORE_RESULT = False

# I use these to debug kombu crashes; we get a more informative message.
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_TASK_RESULT_EXPIRES = 432000

# Sometimes, Ask asks us to enable this to debug issues.
# BTW, it will save some CPU cycles.
CELERY_DISABLE_RATE_LIMITS = False
CELERY_SEND_TASK_EVENTS = True
CELERY_WORKER_DISABLE_RATE_LIMITS = False
CELERY_WORKER_SEND_TASK_EVENTS = True
GEONODE_EXCHANGE = Exchange("default", type="direct", durable=True)
GEOSERVER_EXCHANGE = Exchange("geonode", type="topic", durable=False)
CELERY_TASK_QUEUES = (
    Queue('default', GEONODE_EXCHANGE, routing_key='default'),
    Queue('geonode', GEONODE_EXCHANGE, routing_key='geonode'),
    Queue('update', GEONODE_EXCHANGE, routing_key='update'),
    Queue('cleanup', GEONODE_EXCHANGE, routing_key='cleanup'),
    Queue('email', GEONODE_EXCHANGE, routing_key='email'),
)

CELERY_TASK_QUEUES += (
    Queue("broadcast", GEOSERVER_EXCHANGE, routing_key="#"),
    Queue("email.events", GEOSERVER_EXCHANGE, routing_key="email"),
    Queue("all.geoserver", GEOSERVER_EXCHANGE, routing_key="geoserver.#"),
    Queue(
        "geoserver.catalog",
        GEOSERVER_EXCHANGE,
        routing_key="geoserver.catalog"),
    Queue(
        "geoserver.data", GEOSERVER_EXCHANGE, routing_key="geoserver.catalog"),
    Queue(
        "geoserver.events",
        GEOSERVER_EXCHANGE,
        routing_key="geonode.geoserver"),
    Queue(
        "notifications.events",
        GEOSERVER_EXCHANGE,
        routing_key="notifications"),
    Queue(
        "geonode.layer.viewer",
        GEOSERVER_EXCHANGE,
        routing_key="geonode.viewer"),
)

# Allow our remote workers to get tasks faster if they have a
# slow internet connection (yes Gurney, I'm thinking of you).
CELERY_MESSAGE_COMPRESSION = 'gzip'

# The default beiing 5000, we need more than this.
CELERY_MAX_CACHED_RESULTS = 32768

# NOTE: I don't know if this is compatible with upstart.
CELERYD_POOL_RESTARTS = True

CELERY_TRACK_STARTED = True
CELERY_SEND_TASK_SENT_EVENT = True
BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_MAX_RETRIES = None
TIME_ZONE = 'UTC'
USE_TZ = True

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"

try:
    from .local_settings import *  #noqa
except Exception as e:
    print(e.message)
