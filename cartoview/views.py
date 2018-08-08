# -*- coding: utf-8 -*-
import requests
from django.shortcuts import render
from pkg_resources import parse_version

from .log_handler import get_logger
from .version import get_current_version

logger = get_logger(__name__)


def check_version(request):
    r = requests.get("https://pypi.org/pypi/cartoview/json")
    _version = parse_version(get_current_version())._version
    release = _version.release
    version = [str(x) for x in release]
    current_version = ".".join(version)
    context = dict(
        latest_version=r.json()["info"]["version"],
        current_version=current_version)
    return render(
        request,
        "cartoview/check_version.js",
        context=context,
        content_type="text/javascript")
