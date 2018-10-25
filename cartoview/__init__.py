__version__ = (1, 8, 5, 'final', 0)
__compatible_with__ = []


def get_current_version():
    from .version import get_version
    return get_version(__version__)
