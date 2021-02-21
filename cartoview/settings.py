# -*- coding: utf-8 -*-
from __future__ import print_function

import ast
import copy
import os
import re
import sys
from distutils.util import strtobool

from kombu import Exchange, Queue

import cartoview

CARTOVIEW_DIR = os.path.abspath(os.path.dirname(cartoview.__file__))
BASE_DIR = os.path.dirname(CARTOVIEW_DIR)
APPS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(CARTOVIEW_DIR), "apps"))
PENDING_APPS = os.path.join(APPS_DIR, "pendingOperation.yml")

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '94msw_@n5h@v6)q6(jvcuf%r4u&2bjc^8^(wyw9zhr5$x0rhzb'

ALLOWED_HOSTS = ['*']

DOCKER = os.getenv('DOCKER', False)

PROJECT_NAME = "cartoview"

SITE_NAME = "CartoView"

SITEURL = os.getenv('SITEURL', "http://localhost/")

ROOT_URLCONF = os.getenv('ROOT_URLCONF', "cartoview.urls")

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'experimental_cartoview',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded")
MEDIA_URL = "/uploaded/"
LOCAL_MEDIA_URL = "/uploaded/"

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(CARTOVIEW_DIR, "templates"), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',
                'django.template.context_processors.tz',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',

                'cartoview.app_manager.context_processors.cartoview_processor',
                'cartoview.app_manager.context_processors.site_logo'
            ],
            'debug': True
        }
    }
]

INSTALLED_APPS = (
    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.gis',
    # simpler approach to tagging with Django
    'taggit',
    # tastypie Api
    'tastypie',
    # django-forms-bootstrap
    'django_forms_bootstrap',
    # CartoView
    'cartoview',
    'cartoview.app_manager.apps.AppManagerConfig',
    'cartoview.site_management'
)

# Django Sites
SITE_ID = 1

# ---
# CartoView Settings
# ---
STATICFILES_DIRS = [
    os.path.join(CARTOVIEW_DIR, "static"),
]

APPS_MENU = False

CARTOVIEW_CONTEXT_PROCESSORS = (
    'cartoview.app_manager.context_processors.cartoview_processor',
    'cartoview.app_manager.context_processors.site_logo'
)
TEMPLATES[0]["OPTIONS"]['context_processors'] += CARTOVIEW_CONTEXT_PROCESSORS

CARTOVIEW_TEST = 'test' in sys.argv or ast.literal_eval(
    os.getenv('CARTOVIEW_TEST', "False")) or 'run_cartoview_test' in sys.argv

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

# if cartoview without cartoview_project_template
CARTOVIEW_STAND_ALONE = strtobool(os.getenv('CARTOVIEW_STAND_ALONE', 'TRUE'))

CARTOVIEW_TEST = 'test' in sys.argv or ast.literal_eval(
    os.getenv('CARTOVIEW_TEST', "False")) or 'run_cartoview_test' in sys.argv

if CARTOVIEW_TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'test.db')
        }
    }

if CARTOVIEW_STAND_ALONE or CARTOVIEW_TEST:
    try:
        from .cartoview_apps_settings import *
    except Exception as e:
        print(f'Error while importing cartoview_apps_settings : {e}')
