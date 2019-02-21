# -*- coding: utf-8 -*-
import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from django.conf import settings

# Create your views here.
from django.views.generic.base import TemplateView

from .provider import GeonodeProvider


class ProfileView(TemplateView):
    template_name = "profile.html"


class GenodeAdapter(OAuth2Adapter):
    provider_id = GeonodeProvider.id
    access_token_url = "{}/o/token/".format(settings.OAUTH_SERVER_BASEURL)
    profile_url = "{}/api/o/v4/tokeninfo".format(settings.OAUTH_SERVER_BASEURL)
    authorize_url = "{}/o/authorize/".format(settings.OAUTH_SERVER_BASEURL)

    def complete_login(self, request, app, token, **kwargs):
        # headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        # resp = requests.get(self.profile_url, headers=headers)
        print(token.token)
        resp = requests.post(self.profile_url, data={"token": token.token})
        extra_data = resp.json()
        reformatted_data = {
            "id": extra_data["user_id"],
            "username": extra_data["issued_to"],
            "first_name": extra_data["issued_to"],
            "last_name": extra_data["issued_to"],
            "email": extra_data["email"],
        }
        return self.get_provider().sociallogin_from_response(request, reformatted_data)


oauth2_login = OAuth2LoginView.adapter_view(GenodeAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(GenodeAdapter)
