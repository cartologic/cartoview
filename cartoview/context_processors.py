from cartoview import __version__


def version(request):
    return {'cartoview_version': __version__}
