from abc import ABC, abstractmethod
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class BaseSession(ABC):
    @classmethod
    @abstractmethod
    def get_session(cls, auth_obj):
        return NotImplemented

    @classmethod
    def requests_retry_session(cls, retries=5,
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


class NoAuthClass(BaseSession):
    def get_session(cls, auth_obj):
        return cls.requests_retry_session()
