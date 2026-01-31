import orjson

from typing import (
    AsyncGenerator,
    Any,
)
from uuid import UUID

from httpx import AsyncClient
from loguru import logger

from .response import NexusResponse
from .responses import *
from .exceptions import *

class NexusClient:
    def __init__(
            self,
            base_url: str,
            request_timeout: int = 60
        ) -> None:
        self._client = AsyncClient(
            base_url = base_url,
            timeout = request_timeout
        )
    
    async def close(self) -> None:
        await self._client.aclose()
    
    def _check_uuid(self, uuid: str) -> UUID:
        try:
            return UUID(uuid)
        except ValueError as e:
            raise InvalidUUIDError(f"{uuid} is not a valid UUID") from e
    
    async def submit(self, pool: str, content: Any, timeout: int | None = None) -> NexusResponse[SubmitResponse]:
        response = await self._client.post(
            f"/api/{pool}/submit/json",
            data = {
                "content": content,
                "timeout": timeout
            }
        )
        return NexusResponse(
            response = response,
            model = SubmitResponse
        )
    
    async def download(self, pool: str, file_uuid: str) -> NexusResponse[DownloadResponse]:
        response = await self._client.get(
            f"/api/{pool}/files/{self._check_uuid(file_uuid)}/download/json"
        )

        return NexusResponse(
            response = response,
            model = DownloadResponse
        )
    
    async def update(self, pool: str, file_uuid: str, content: Any, timeout: int | None = None) -> NexusResponse[UpdateResponse]:
        response = await self._client.put(
            f"/api/{pool}/files/{self._check_uuid(file_uuid)}/update",
            json = {
                "content": content,
                "timeout": timeout
            }
        )
        return NexusResponse(
            response = response,
            model = UpdateResponse
        )
    
    async def list(self, pool: str) -> AsyncGenerator[str, None]:
        response = await self._client.get(
            f"/api/{pool}/files/list/json"
        )
        async for line in response.aiter_lines():
            try:
                data = orjson.loads(line)
            except orjson.JSONDecodeError:
                logger.warning(
                    "Failed to decode line: {line}",
                    line = line
                )
                continue

            if isinstance(data, str):
                yield data
            else:
                logger.warning(
                    "Invalid data type: {data}(type: {type})",
                    data = data,
                    type = type(data).__name__
                )
    
    async def remove(self, pool: str, file_uuid: str) -> NexusResponse[RemoveResponse]:
        response = await self._client.delete(
            f"/api/{pool}/files/{self._check_uuid(file_uuid)}/remove"
        )
        return NexusResponse(
            response = response,
            model = RemoveResponse
        )