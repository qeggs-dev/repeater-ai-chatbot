from urllib.parse import urlparse
from typing import Iterable
from dataclasses import dataclass, field

from pythonping import ping
from pythonping.executor import ResponseList

@dataclass
class Detail:
    url: str
    timeout: int = 2
    times: int = 4
    size: int = 32
    interval: int = 0

    @property
    def host(self) -> str | None:
        return urlparse(self.url).hostname

@dataclass
class Response:
    host: str = ""
    responses: ResponseList = field(default_factory = ResponseList)

def send_ping(providers: Iterable[Detail]) -> list[Response]:
    responses: list[ResponseList] = []
    for provider in providers:
        if not provider.host:
            continue
        response_list: ResponseList = ping(
            provider.host,
            timeout = provider.timeout,
            count = provider.times,
            size = provider.size,
            interval = provider.interval
        )
        response = Response(
            host = provider.host,
            responses = response_list
        )
        responses.append(response)
    return responses