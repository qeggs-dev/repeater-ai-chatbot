import ssl
import httpx
from ._model import RenderResponse
from ...http_response import Response

class HTMLRenderClient:
    def __init__(self, base_url: str, timeout: int, verify: ssl.SSLContext | str | bool = True):
        self._base_url = base_url
        self._timeout = timeout
        self._client = httpx.AsyncClient(
            base_url = base_url,
            timeout = timeout,
            verify = verify
        )
    
    async def render(self, text: str) -> Response[RenderResponse]:
        """Render markdown text to HTML."""
        response = await self._client.post(
            "/render",
            json = {
                "content": text
            }
        )
        return Response(
            response = response,
            model = RenderResponse
        )
