# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from urllib.parse import urlencode

import dj_database_url
from django.conf import settings
from future import standard_library

standard_library.install_aliases()


class DBParseException(Exception):
    pass


def get_db_url(db_key):
    databases = getattr(settings, 'DATABASES', {})
    _schemes = {v: k for k, v in dj_database_url.SCHEMES.items()}
    if db_key in databases:
        db = databases.get(db_key)
        engine = db.get('ENGINE', None)
        db_url = ''
        name = db.get('NAME', None)
        host = db.get('HOST', None)
        port = db.get('PORT', None)
        user = db.get('USER', None)
        password = db.get('PASSWORD', None)
        options = db.get('OPTIONS', None)
        if db and engine:
            if engine != dj_database_url.SCHEMES[
                    'sqlite'] and engine != dj_database_url.SCHEMES[
                    'spatialite']:
                db_url += "{}://".format(_schemes[engine])
                if user and password:
                    db_url += "{}:{}".format(user, password)
                if host:
                    db_url += "@{}".format(host)
                if port:
                    db_url += ":{}".format(port)
                if name:
                    db_url += "/{}".format(name)
                if options:
                    db_url += "?{}".format(urlencode(options))
            else:
                db_url += "{}://".format(_schemes[engine])
                db_url += name
        return db_url
    raise DBParseException("Invalid database key")
