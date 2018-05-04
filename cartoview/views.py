# -*- coding: utf-8 -*-
import requests
from django.shortcuts import render
from .version import (get_current_version)
from .log_handler import get_logger
logger = get_logger(__name__)


def index(request):
    context = {}
    return render(request, 'site_index.html', context)


def check_version(request):
    r = requests.get("https://pypi.org/pypi/cartoview/json")
    context = dict(
        latest_version=r.json()["info"]["version"],
        current_version=get_current_version())
    return render(
        request,
        "cartoview/check_version.js",
        context=context,
        content_type="text/javascript")
