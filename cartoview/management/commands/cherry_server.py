# -*- coding: utf-8 -*-

import importlib
import os

import cherrypy
from django.core.management.base import BaseCommand

_current_path = os.path.abspath(os.path.dirname(__file__))
_default_config = os.path.join(_current_path, 'cherry.conf')


class Command(BaseCommand):
    help = 'Start Django Server'

    def add_arguments(self, parser):
        parser.add_argument(
            '-w',
            '--wsgi',
            type=str,
            dest='wsgi',
            nargs='?',
            default='cartoview.wsgi',
            help='Wsgi Module')

        parser.add_argument(
            '-sf',
            '--config-file',
            type=str,
            dest='config_file',
            nargs='?',
            default=_default_config,
            help='Socket File')

    def handle(self, *args, **options):
        config_file = options.get('config_file')
        wsgi_module = options.get('wsgi')
        wsgi_app = importlib.import_module(wsgi_module).application
        if os.path.exists(config_file):
            self.start_server(wsgi_app, config_file)
        else:
            raise Exception("Can't find/access config file")

    def start_server(self, wsgi_app, config_file):
        cherrypy.tree.graft(wsgi_app, "/")
        cherrypy.config.update(config_file)
        cherrypy.engine.start()
        cherrypy.engine.block()
