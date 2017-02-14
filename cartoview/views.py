from django.shortcuts import render, render_to_response, HttpResponse
import requests
from geonode.version import get_version
from cartoview import __version__

def index(request):
    context = {}
    return render(request, 'site_index.html', context)


def check_version(request):
    r = requests.get("http://pypi.python.org/pypi/cartoview/json")
    context = dict(latest_version=r.json()["info"]["version"], current_version=get_version(__version__))
    return render(request, "cartoview/check_version.js", context=context,content_type="text/javascript")
