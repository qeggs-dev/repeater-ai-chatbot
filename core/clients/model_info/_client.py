import ssl
import httpx

from urllib.parse import quote
from .responses import (
    ModelInfoResponse,
    DisableResponse
)
from ...special_exception import HTTPException
from ...http_response import Response

class ModelsClient:
    def __init__(
            self,
            base_url: str,
            api_key: str | None = None,
            timeout: int | None = None,
            verify: ssl.SSLContext | str | bool = True,
            transport: httpx.AsyncHTTPTransport | None = None,
        ):
        self._base_url = base_url
        self._client = httpx.AsyncClient(
            base_url = self._base_url,
            timeout = timeout,
            headers = {
                "Authorization": f"Bearer {api_key}"
            },
            verify = verify,
            transport = transport
        )
    
    async def get_models(self, model_id: str) -> Response[ModelInfoResponse]:
        try:
            http_response = await self._client.get(
                f"/models/{quote(model_id)}"
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
    
    async def disable(self, model_id: str, timeout: int) -> Response[DisableResponse]:
        try:
            http_response = await self._client.post(
                f"/disable/{quote(model_id)}",
                json = {
                    "timeout": timeout
                }
            )
        except httpx.RequestError as e:
            raise HTTPException(detail = f"Disable Model API Failed: {e}") from e

        response = Response(
            response = http_response,
            model = DisableResponse
        )

        return response