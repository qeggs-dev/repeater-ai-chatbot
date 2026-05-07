from pydantic import BaseModel
from httpx import AsyncClient, Limits, Timeout
from ...auxiliary.http import ClientTimeout, ClientLimits, get_ssl_context

class ClientInfo(BaseModel, frozen=True):
    url: str
    proxy: str | None = None
    timeout: int | float | ClientTimeout = 5.0
    limits: ClientLimits | None = None
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
            proxy = self.proxy,
            verify = get_ssl_context(),
            limits = limits,
            timeout = timeout,
            default_encoding = self.encoding
        )
        return client