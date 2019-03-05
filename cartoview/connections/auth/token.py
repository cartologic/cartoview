from .base import BaseSession
import requests


class TokenAuthSession(BaseSession):
    @classmethod
    def get_session(cls, auth_obj):
        session = requests.Session()
        headers = {}
        if auth_obj.prefix and auth_obj.prefix != "":
            headers['Authorization'] = "{} {}".format(auth_obj.prefix,
                                                      auth_obj.token)
        else:
            headers['Authorization'] = "{}".format(auth_obj.token)
        session.headers.update(headers)
        return cls.requests_retry_session(session=session)
