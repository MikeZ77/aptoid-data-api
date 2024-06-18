import abc

import httpx


class AbstractHttpRequests(abc.ABC):
    @abc.abstractmethod
    def get(self, url: str, **kwargs):
        raise NotImplementedError


class HttpRequests(AbstractHttpRequests):
    def __init__(self):
        self.request = httpx

    def get(self, url: str, **kwargs):
        self.request.get(url, **kwargs)
