from geonode.version import get_version
from cartoview import __compatible_with__, __version__
import json


def get_current_version():
    return get_version(__version__)


def get_backward_compatible():
    backward_compatible = [
        get_version(version) for version in __compatible_with__
    ]
    return backward_compatible


def json_version_info():
    info = {
        'current_version': get_current_version(),
        'backward_versions': get_backward_compatible()
    }
    return json.dumps(info)
