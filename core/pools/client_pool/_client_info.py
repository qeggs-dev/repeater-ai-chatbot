from pydantic import BaseModel
from httpx import AsyncClient

class ClientInfo(BaseModel, frozen=True):
    url: str
    proxy: str | None = None
    timeout: int | float = 5.0
    encoding: str = "utf-8"

    def to_client(self) -> AsyncClient:
        client = AsyncClient(
            base_url = self.url,
            proxy = self.proxy,
            timeout = self.timeout,
            default_encoding = self.encoding
        )
        return client