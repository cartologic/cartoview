# -*- coding: utf-8 -*-
import requests
from django.http import HttpResponse
from django.shortcuts import render
from .version import (get_current_version)


def index(request):
    context = {}
    return render(request, 'site_index.html', context)


def check_version(request):
    r = requests.get("http://pypi.python.org/pypi/cartoview/json",)
    context = dict(
        latest_version=r.json()["info"]["version"],
        current_version=get_current_version())
    return render(
        request,
        "cartoview/check_version.js",
        context=context,
        content_type="text/javascript")
