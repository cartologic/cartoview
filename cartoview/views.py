# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import requests
from geonode.version import get_version
from cartoview import __compatible_with__, __version__
import json


def index(request):
    context = {}
    return render(request, 'site_index.html', context)


def check_version(request):
    r = requests.get("http://pypi.python.org/pypi/cartoview/json")
    context = dict(
        latest_version=r.json()["info"]["version"],
        current_version=get_version(__version__))
    return render(
        request,
        "cartoview/check_version.js",
        context=context,
        content_type="text/javascript")


def version_info(request):
    backward_compatible = [
        get_version(version) for version in __compatible_with__
    ]
    info = {
        'current_version': get_version(__version__),
        'backward_versions': backward_compatible
    }
    return HttpResponse(content=json.dumps(info),
                        content_type='application/json')
