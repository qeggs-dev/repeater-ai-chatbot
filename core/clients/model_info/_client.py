import ssl
import httpx

from urllib.parse import quote
from ._response import ModelInfoResponse
from ...special_exception import HTTPException
from ...http_response import Response

class ModelsClient:
    def __init__(self, base_url: str, timeout: int | None = None, verify: ssl.SSLContext | str | bool = True):
        self._base_url = base_url
        self._client = httpx.AsyncClient(
            base_url = self._base_url,
            timeout = timeout,
            verify = verify
        )
    
    async def get_models(self, model_uid: str) -> Response[ModelInfoResponse]:
        try:
            http_response = await self._client.get(
                f"/models/{quote(model_uid)}"
            )
        except httpx.RequestError as e:
            raise HTTPException(detail = f"Get Models API Failed: {e}") from e
        
        response = Response(
            response = http_response,
            model = ModelInfoResponse
        )

        return response
    
    async def get_all_models(self) -> Response[ModelInfoResponse]:
        try:
            http_response = await self._client.get(
                "/models"
            )
        except httpx.RequestError as e:
            raise HTTPException(detail = f"Get All Models API Failed: {e}") from e

        response = Response(
            response = http_response,
            model = ModelInfoResponse
        )

        return response