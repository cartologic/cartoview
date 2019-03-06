# -*- coding: utf-8 -*-
from collections import namedtuple
ServerType = namedtuple('ServerType', ['name', 'value', 'title'])
ESRI = ServerType("ARCGIS_SERVER", "ESRI", "ArcGIS Server")
MAPSERVER = ServerType("MAPSERVER", "MS", "MapServer")
GEOSERVER = ServerType("GEOSERVER", "GS", "Geoserver")
GEONODE = ServerType("GEONODE", "G", "Geonode")
SUPPORTED_SERVERS = (
    ESRI,
    MAPSERVER,
    GEOSERVER,
    GEONODE,
)
DEFAULT_PROXY_SETTINGS = {
    "default_headers": {
        "Accept": "*",
        "Accept-Language": "*",
    }
}
