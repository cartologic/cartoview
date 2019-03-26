# -*- coding: utf-8 -*-
from collections import namedtuple
ServerType = namedtuple('ServerType', ['name', 'value', 'title', 'type'])
ESRI = ServerType("ARCGIS_SERVER", "ESRI", "ArcGIS Server", "arcgis")
MAPSERVER = ServerType("OGC-WMS", "OGC-WMS", "OGC Web Map Service", "wms")
GEOSERVER = ServerType("OGC-WFS", "OGC-WFS", "OGC Web Feature Service", "wfs")
GEONODE = ServerType("GEONODE", "G", "Geonode", "geonode")
GEOJSON = ServerType("GEOJSON", "GEOJSON", "GeoJSON", "geojson")
KML = ServerType("KML", "KML", "KML", "kml")
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
    },
    "timeout": 5,
}
default_app_config = 'cartoview.connections.apps.ConnectionsConfig'
