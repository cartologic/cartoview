from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import warnings

from django.conf.urls import include, url
from django.shortcuts import render
from future import standard_library
from tastypie.api import Api as TastypieApi
from tastypie.utils import trailing_slash

from cartoview.log_handler import get_logger
from .serializers import HTMLSerializer

logger = get_logger(__name__)
standard_library.install_aliases()


def home(request):
    return render(request, 'app_manager/rest_api/home.html',
                  {'apis': sorted(rest_api.apis.keys())})


class BaseApi(TastypieApi):
    """
    A version of the Api that doesn't require a name.
    It also uses the whippedcream serializer by default.
    """

    def __init__(self, app_name):
        self.app_name = app_name
        super(BaseApi, self).__init__('', HTMLSerializer)

    @property
    def urls(self):
        """
        Provides URLconf details for the ``Api`` and all registered
        ``Resources`` beneath it.
        """
        if self.api_name:
            api_pattern = '(?P<api_name>%s)'
            top_level = r"^%s%s$" % (api_pattern, trailing_slash())
        else:
            api_pattern = '(?P<api_name>)'
            top_level = r"^$"

        pattern_list = [
            url(top_level,
                self.wrap_view('top_level'),
                name="%s_rest_url" % self.app_name),
        ]

        for name in sorted(self._registry.keys()):
            resource = self._registry[name]
            resource.api_name = self.api_name
            pattern_list.append(
                url(r"^%s" % api_pattern, include(resource.urls)))

        urlpatterns = self.prepend_urls()
        overridden_urls = self.override_urls()
        if overridden_urls:
            warnings.warn(
                "'override_urls' is a deprecated method & \
                will be removed by v1.0.0.\
                 Please rename your method to ``prepend_urls``."
            )

            urlpatterns += overridden_urls

        urlpatterns += pattern_list
        return urlpatterns


class Api(object):

    def __init__(self):
        self.apis = {}

    def register(self, resource, app_name=None, canonical=True):
        module_name = resource.__module__

        if app_name is None:
            try:
                app_name = module_name.split('.')[1]
            except BaseException as e:
                logger.error(e)
        if app_name not in self.apis:
            self.apis[app_name] = BaseApi(app_name)
        self.apis[app_name].register(resource, canonical)

    @property
    def urls(self):
        pattern_list = [
            url(r'^$',
                home,
                name='cartoview_rest_url'),
        ]
        for name in sorted(self.apis.keys()):
            pattern_list.append(
                url(r"^%s/" % name, include(self.apis[name].urls)))
        self.urlpatterns = pattern_list
        return self.urlpatterns

    def register_app_urls(self, app_name):
        self.urlpatterns.append(
            url(r"^%s/" % app_name, include(self.apis[app_name].urls)))


rest_api = Api()
