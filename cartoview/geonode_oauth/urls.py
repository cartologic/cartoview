# -*- coding: utf-8 -*-
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import GeonodeProvider

urlpatterns = default_urlpatterns(GeonodeProvider)
