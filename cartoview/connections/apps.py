# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConnectionsConfig(AppConfig):
    name = 'cartoview.connections'
    verbose_name = _('Connections')
