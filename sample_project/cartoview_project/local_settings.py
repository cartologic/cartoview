# -*- coding: utf-8 -*-
SITE_NAME = "Cartoview Demo"
SITEURL = 'http://localhost:8004/'
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'cartoview_web',
        'USER': 'postgres',
        'PASSWORD': '',
        'PORT' : '',
        'HOST' : '',
    },
    'datastore': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'cartoview_datastore',
        'USER': 'postgres',
        'PASSWORD': '',
        'PORT' : '',
        'HOST' : '',
    }
}
GEOSERVER_URL = 'http://localhost:8080/geoserver/'
GEOSERVER_PUBLIC_URL = 'http://localhost:8080/geoserver/'
GEOSERVER_DATASTORE = 'datastore'

REGISTRATION_OPEN = True
# ACCOUNT_EMAIL_CONFIRMATION_EMAIL = True
# ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
# ACCOUNT_APPROVAL_REQUIRED = False

# Email for users to contact admins.
THEME_ACCOUNT_CONTACT_EMAIL = 'admin@cartologic.com'

