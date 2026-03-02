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
    
    async def submit(self, pool: str, content: dict[str, Any], timeout: int | None = None) -> NexusResponse[SubmitResponse]:
        logger.info(
            "Submitting content to {pool}",
            pool = pool
        )
        response = await self._client.post(
            f"/api/{pool}/submit",
            json = {
                "content": content,
                "timeout": timeout
            }
        )
        return NexusResponse(
            response = response,
            model = SubmitResponse
        )
    
    async def download(self, pool: str, resources_uuid: str, data_id: str) -> NexusResponse[DownloadResponse]:
        logger.info(
            "Downloading file {resources_uuid} from {pool}",
            resources_uuid = resources_uuid,
            pool = pool
        )
        response = await self._client.get(
            f"/api/{pool}/resources/{self._check_uuid(resources_uuid)}/download/{data_id}"
        )

        return NexusResponse(
            response = response,
            model = DownloadResponse
        )
    
    async def update(self, pool: str, resources_uuid: str, content: dict[str, Any], timeout: int | None = None) -> NexusResponse[UpdateResponse]:
        logger.info(
            "Updating file {resources_uuid} in {pool}",
            resources_uuid = resources_uuid,
            pool = pool
        )
        response = await self._client.put(
            f"/api/{pool}/resources/{self._check_uuid(resources_uuid)}/update",
            json = {
                "content": content,
                "timeout": timeout
            }
        )
        return NexusResponse(
            response = response,
            model = UpdateResponse
        )
    
    async def resources_list(self, pool: str) -> list[str]:
        logger.info(
            "Getting resources list in {pool}",
            pool = pool
        )
        response = await self._client.get(
            f"/api/{pool}/resources_list"
        )
        data = response.json()
        if not isinstance(data, list):
            raise ResponseTypeError(
                "Invalid response from server"
            )
        return data
    
    async def resources_list_stream(self, pool: str) -> AsyncGenerator[str, None]:
        logger.info(
            "Getting resources list in {pool}",
            pool = pool
        )
        response = await self._client.get(
            f"/api/{pool}/resources_list/stream"
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
    
    async def data_list(self, pool: str, resource: str) -> list[str]:
        logger.info(
            "Getting data list in {pool}/{resource}",
            pool = pool,
            resource = resource
        )
        response = await self._client.get(
            f"/api/{pool}/data_list/{resource}"
        )
        data = await response.json()
        if not isinstance(data, list):
            raise TypeError(
                "Invalid response from server"
            )
        return data
    
    async def data_list_stream(self, pool: str, resource: str) -> AsyncGenerator[str, None]:
        logger.info(
            "Getting data list in {pool}/{resource}",
            pool = pool,
            resource = resource
        )
        response = await self._client.get(
            f"/api/{pool}/data_list/{resource}"
        )
        async for line in response.aiter_lines():
            data = orjson.loads(line)
            if not isinstance(data, str):
                logger.warning(
                    "Invalid response from server"
                )
                continue
            yield data
    
    async def remove(self, pool: str, file_uuid: str) -> NexusResponse[RemoveResponse]:
        logger.info(
            "Removing file {file_uuid} from {pool}",
            file_uuid = file_uuid,
            pool = pool
        )
        response = await self._client.delete(
            f"/api/{pool}/resources/{self._check_uuid(file_uuid)}/remove/resource"
        )
        return NexusResponse(
            response = response,
            model = RemoveResponse
        )
    
    async def remove_data(self, pool: str, file_uuid: str, data_id: str) -> NexusResponse[RemoveResponse]:
        logger.info(
            "Removing file {file_uuid} from {pool}",
            file_uuid = file_uuid,
            pool = pool
        )
        response = await self._client.delete(
            f"/api/{pool}/resources/{self._check_uuid(file_uuid)}/remove/data/{data_id}"
        )
        return NexusResponse(
            response = response,
            model = RemoveResponse
        )