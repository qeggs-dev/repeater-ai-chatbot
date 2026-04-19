from pydantic import BaseModel
from openai import AsyncOpenAI
from loguru import logger

class ClientInfo(BaseModel, frozen=True):
    url: str
    key: str
    timeout: int | float | None = 600.0

    def to_openai_client(self) -> AsyncOpenAI:
        client = AsyncOpenAI(
            base_url = self.url,
            api_key = self.key,
            timeout = self.timeout,
        )
        return client