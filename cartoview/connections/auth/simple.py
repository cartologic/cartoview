from functools import lru_cache

import requests

from .base import BaseSession


class BasicAuthSession(BaseSession):
    @classmethod
    @lru_cache(maxsize=256)
    def get_session(cls, auth_obj):
        session = requests.Session()
        session.auth = requests.auth.HTTPBasicAuth(
            auth_obj.username, auth_obj.password)
        return cls.requests_retry_session(session=session)


class DigestAuthSession(BaseSession):
    @classmethod
    @lru_cache(maxsize=256)
    def get_session(cls, auth_obj):
        session = requests.Session()
        session.auth = requests.auth.HTTPDigestAuth(
            auth_obj.username, auth_obj.password)
        return cls.requests_retry_session(session=session)
