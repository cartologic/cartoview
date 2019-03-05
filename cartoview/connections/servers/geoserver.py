# -*- coding: utf-8 -*-
import requests
from owslib.wms import WebMapService

from cartoview.log_handler import get_logger

from ...connections.utils import urljoin
from .base import BaseServer

logger = get_logger(__name__)


class Geoserver(BaseServer):
    @property
    def is_alive(self):
        req = self.session.get(self.status_url)
        logger.info(self.status_url)
        logger.info(req.status_code)
        if req.status_code == requests.codes['ok']:
            return True
        else:
            return False

    @property
    def wms_service(self):
        wms = WebMapService(self.wms_url, version='1.1.1')
        return wms

    def get_layers(self):
        wms = self.wms_service
        items = wms.items()
        layers = [l[1] for l in items]
        return layers

    @property
    def wms_url(self):
        return urljoin(self.url, 'wms')

    @property
    def status_url(self):
        return urljoin(self.rest, 'about/status')

    @property
    def rest(self):
        return urljoin(self.url, 'rest')
