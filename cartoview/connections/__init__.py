# -*- coding: utf-8 -*-
from collections import namedtuple
ServerType = namedtuple('ServerType', ['name', 'value', 'title'])
ESRI = ServerType("ARCGIS_SERVER", "ESRI", "ArcGIS Server")
MAPSERVER = ServerType("MAPSERVER", "MS", "MapServer")
GEOSERVER = ServerType("GEOSERVER", "GS", "Geoserver")
GEONODE = ServerType("GEONODE", "G", "Geonode")
GEOJSON = ServerType("GEOJSON", "GEOJSON", "GeoJSON")
KML = ServerType("KML", "KML", "KML")
SUPPORTED_SERVERS = (
    ESRI,
    MAPSERVER,
    GEOSERVER,
    GEONODE,
    GEOJSON,
    KML
)
DEFAULT_PROXY_SETTINGS = {
    "default_headers": {
        "Accept": "*",
        "Accept-Language": "*",
    }
}
default_app_config = 'cartoview.connections.apps.ConnectionsConfig'
