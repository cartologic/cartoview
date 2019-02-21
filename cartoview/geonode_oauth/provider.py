# -*- coding: utf-8 -*-
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class GeonodeAccount(ProviderAccount):
    pass


class GeonodeProvider(OAuth2Provider):

    id = "geonodeprovider"
    name = "Geonode OAuth2 Provider"
    account_class = GeonodeAccount

    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        return dict(
            username=data["username"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )

    def get_default_scope(self):
        # scope = ["read", "write"]
        scope = ["write"]
        return scope


providers.registry.register(GeonodeProvider)
