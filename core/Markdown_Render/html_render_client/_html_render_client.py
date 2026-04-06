import httpx
from ._model import Render_Response
from ...Response import Response

class HTMLRenderClient:
    def __init__(self, base_url: str, timeout: int):
        self._base_url = base_url
        self._timeout = timeout
        self._client = httpx.AsyncClient(
            base_url = base_url,
            timeout = timeout
        )
    
    async def render(self, text: str) -> Response[Render_Response]:
        """Render markdown text to HTML."""
        response = await self._client.post(
            "/render",
            json = {
                "content": text
            }
        )
        return Response(
            response = response,
            model = Render_Response
        )
