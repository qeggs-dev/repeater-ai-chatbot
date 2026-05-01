from pydantic import BaseModel
from httpx import AsyncClient
from ...runtime_container import get_ssl_context

class ClientInfo(BaseModel, frozen=True):
    url: str
    proxy: str | None = None
    timeout: int | float = 5.0
    max_connections: int = 100
    max_keepalive_connections: int = 20
    keepalive_expiry: int = 60
    encoding: str = "utf-8"

    def to_client(self) -> AsyncClient:
        client = AsyncClient(
            base_url = self.url,
            proxy = self.proxy,
            timeout = self.timeout,
            max_connections = self.max_connections,
            max_keepalive_connections = self.max_keepalive_connections,
            keepalive_expiry = self.keepalive_expiry,
            verify = get_ssl_context(),
            default_encoding = self.encoding
        )
        return client