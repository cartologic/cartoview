from .geoserver import Geoserver


class MapServer(Geoserver):
    @property
    def status_url(self):
        return self.rest

    @property
    def rest(self):
        return self.url
