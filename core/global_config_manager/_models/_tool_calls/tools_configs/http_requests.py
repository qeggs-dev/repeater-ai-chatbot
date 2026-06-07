from pydantic import BaseModel
from .._http_methods import HTTPMethods
from typing import Literal

class HTTPRequests(BaseModel):
    robots_cache_size: int = 8192
    robots_cache_timeout: int = 3600
    allowed_http_methods: list[HTTPMethods] | Literal["ALL"] | None = None
    allow_private_network_requests: bool = False