from .celery import app

__version__ = (1, 8, 2, 'rc', 0)
__compatible_with__ = []


def get_current_version():
    import geonode.version
    return geonode.version.get_version(__version__)
