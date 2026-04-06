import httpx

from ._models import ModelAPIResponse, StaticModelAPIResponse, APIKeyResponse, ExceptionResponse
from ._model_type import ModelType
from typing import Literal, overload

class ModelsClient:
    def __init__(self, base_url: str, timeout: int | None = None):
        self._base_url = base_url
        self._client = httpx.AsyncClient(
            base_url = self._base_url,
            timeout = timeout
        )
    
    @overload
    async def get_models(self, model_type: ModelType, with_api_key: Literal[True] = True) -> StaticModelAPIResponse | ExceptionResponse:
        ...
    
    @overload
    async def get_models(self, model_type: ModelType, with_api_key: Literal[False] = False) -> ModelAPIResponse | ExceptionResponse:
        ...
    
    async def get_models(self, model_type: ModelType, with_api_key: bool = False) -> ModelAPIResponse | StaticModelAPIResponse | ExceptionResponse:
        response = await self._client.get(
            f"/model_info/{model_type.value}",
            params = {
                "with_api_key": with_api_key
            }
        )

        if response.status_code == 500:
            return ExceptionResponse(
                **response.json()
            )
        
        if with_api_key:
            return StaticModelAPIResponse(
                **response.json()
            )
        else:
            return ModelAPIResponse(
                **response.json()
            )
    
    @overload
    async def get_model(self, model_type: ModelType, model_uid: str, with_api_key: Literal[True] = True) -> StaticModelAPIResponse | ExceptionResponse:
        ...
    
    @overload
    async def get_model(self, model_type: ModelType, model_uid: str, with_api_key: Literal[False] = False) -> ModelAPIResponse | ExceptionResponse:
        ...
    
    async def get_model(self, model_type: ModelType, model_uid: str, with_api_key: bool = False) -> ModelAPIResponse | StaticModelAPIResponse | ExceptionResponse:
        response = await self._client.get(
            f"/model_info/{model_type.value}/{model_uid}",
            params = {
                "with_api_key": with_api_key
            }
        )

        if response.status_code == 500:
            return ExceptionResponse(
                **response.json()
            )
        
        if with_api_key:
            return StaticModelAPIResponse(
                **response.json()
            )
        else:
            return ModelAPIResponse(
                **response.json()
            )
    
    async def get_api_key(self) -> APIKeyResponse | ExceptionResponse:
        response = await self._client.get(
            "/api_key"
        )
        if response.status_code == 500:
            return ExceptionResponse(
                **response.json()
            )
        return APIKeyResponse(
            **response.json()
        )
    
    async def close(self):
        await self._client.aclose()