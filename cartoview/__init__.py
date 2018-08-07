from .celery import app

__version__ = (1, 8, 2, 'rc', 3)
__compatible_with__ = []


def get_current_version():
    from .version import get_version
    return get_version(__version__)
