from django.conf import settings
from revproxy.views import ProxyView


class ProxyViewMixin:
    netloc = getattr(settings, 'OAUTH_SERVER_BASEURL', None)


class GeoNodeApiProxyView(ProxyViewMixin, ProxyView):
    upstream = f'{ProxyViewMixin.netloc}api/'


class GeoServerProxyView(ProxyViewMixin, ProxyView):
    upstream = f'{ProxyViewMixin.netloc}geoserver/'
