# -*- coding: utf-8 -*-
import requests
from allauth.socialaccount.models import SocialToken
from django.conf import settings
from django.utils import timezone
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from cartoview.log_handler import get_logger
logger = get_logger(__name__)


def requests_retry_session(retries=3,
                           backoff_factor=1,
                           status_forcelist=(502, 503, 504),
                           session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        method_whitelist=frozenset(['GET', 'POST', 'PUT', 'DELETE', 'HEAD']))
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class OAuthUtils(object):
    def __init__(self, provider="geonodeprovider"):
        self.provider = provider

    def token_is_valid(self, token):
        valid = False
        if token and (token.expires_at > timezone.now()):
            valid = True
        return valid

    def _refresh_payload(self, token):
        client_id = token.app.client_id
        client_secret = token.app.secret
        grant_type = 'refresh_token'
        refresh_token = token.token_secret
        data = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token
        }
        return data

    def update_token(self, token, new_token_data):
        token.token = new_token_data['access_token']
        token.token_secret = new_token_data['refresh_token']
        token.expires_at = timezone.now(
        ) + timezone.timedelta(seconds=int(new_token_data['expires_in']))
        token.save()
        return token

    def refresh_token(self, token):
        session = requests_retry_session()
        url = '{}{}'.format(settings.OAUTH_SERVER_BASEURL, '/o/token/')
        req = session.post(url, data=self._refresh_payload(token))
        msg = "url: {} \t status_code: {}".format(req.url, req.status_code)
        logger.info(msg)
        if req.status_code == 401:
            logger.error(req.text)
            raise Exception("Your Token expired please login again")
        if req.status_code != 200:
            raise Exception("Failed to refresh token")
        else:
            token = self.update_token(token, req.json())
        return token

    def get_access_token(self, user):
        access_token = SocialToken.objects.get(
            account__user=user, account__provider=self.provider)
        if not self.token_is_valid(access_token):
            access_token = self.refresh_token(access_token)
        return access_token.token

    def get_requests_session(self, user):
        token = self.get_access_token(user)
        session = requests.Session()
        auth_header = {'Authorization': 'Bearer {}'.format(token)}
        session.headers.update(auth_header)
        return requests_retry_session(session=session)


geonode_oauth_utils = OAuthUtils()
