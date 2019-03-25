from requests.adapters import HTTPAdapter


class TimeoutSupportAdapter(HTTPAdapter):
    def __init__(self, timeout=10, *args, **kwargs):
        self.timeout = timeout
        super(TimeoutSupportAdapter, self).__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        timeout = kwargs.get("timeout", self.timeout)
        kwargs.update({"timeout": timeout})
        return super(TimeoutSupportAdapter, self).send(*args, **kwargs)
