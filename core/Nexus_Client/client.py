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
        logger.info(
            "Submitting content to {pool}",
            pool = pool
        )
        response = await self._client.post(
            f"/api/{pool}/submit/json",
            json = {
                "content": content,
                "timeout": timeout
            }
        )
        return NexusResponse(
            response = response,
            model = SubmitResponse
        )
    
    async def download(self, pool: str, file_uuid: str) -> NexusResponse[DownloadResponse]:
        logger.info(
            "Downloading file {file_uuid} from {pool}",
            file_uuid = file_uuid,
            pool = pool
        )
        response = await self._client.get(
            f"/api/{pool}/files/{self._check_uuid(file_uuid)}/download/json"
        )

        return NexusResponse(
            response = response,
            model = DownloadResponse
        )
    
    async def update(self, pool: str, file_uuid: str, content: Any, timeout: int | None = None) -> NexusResponse[UpdateResponse]:
        logger.info(
            "Updating file {file_uuid} in {pool}",
            file_uuid = file_uuid,
            pool = pool
        )
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
    
    async def list(self, pool: str) -> list[str]:
        logger.info(
            "Listing files in {pool}",
            pool = pool
        )
        response = await self._client.get(
            f"/api/{pool}/list"
        )
        data = response.json()
        if not isinstance(data, list):
            raise ResponseTypeError(
                "Invalid response from server"
            )
        return data
    
    async def list_stream(self, pool: str) -> AsyncGenerator[str, None]:
        logger.info(
            "Listing files in {pool}",
            pool = pool
        )
        response = await self._client.get(
            f"/api/{pool}/list/stream"
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
        logger.info(
            "Removing file {file_uuid} from {pool}",
            file_uuid = file_uuid,
            pool = pool
        )
        response = await self._client.delete(
            f"/api/{pool}/files/{self._check_uuid(file_uuid)}/remove"
        )
        return NexusResponse(
            response = response,
            model = RemoveResponse
        )