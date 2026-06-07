from pydantic import BaseModel
from typing import Any
from httpx import AsyncClient, Limits, Timeout
from ...auxiliary.http import ClientTimeout, ClientLimits, get_ssl_context

class ClientInfo(BaseModel, frozen=True):
    url: str = ""
    params: dict[str, str] | None = None
    headers: dict[str, str] | None = None
    cookies: dict[str, str] | None = None
    auth: tuple[str, str] | None = None
    proxy: str | None = None
    limits: ClientLimits | None = None
    follow_redirects: bool = True
    timeout: int | float | ClientTimeout = 5.0
    encoding: str = "utf-8"

    def _default_limits(self) -> Limits:
        return Limits(
            max_connections = 100,
            max_keepalive_connections = 20
        )
    
    def _default_timeout(self) -> Timeout:
        return Timeout(
            timeout = 5.0
        )

    def to_client(self) -> AsyncClient:
        if self.limits is None:
            limits = self._default_limits()
        else:
            limits = self.limits.to_limits()
        
        if isinstance(self.timeout, int | float):
            timeout = self.timeout
        elif isinstance(self.timeout, ClientTimeout):
            timeout = self.timeout.to_timeout()
        else:
            timeout = self._default_timeout()
        
        client = AsyncClient(
            base_url = self.url,
            auth = self.auth,
            params = self.params,
            headers = self.headers,
            cookies = self.cookies,
            proxy = self.proxy,
            follow_redirects = self.follow_redirects,
            verify = get_ssl_context(),
            limits = limits,
            timeout = timeout,
            default_encoding = self.encoding
        )
        return client