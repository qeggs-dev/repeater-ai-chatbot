import httpx

class HTMLRenderClient:
    def __init__(self, base_url: str, timeout: int):
        self._base_url = base_url
        self._timeout = timeout
        self._client = httpx.AsyncClient(
            base_url = base_url,
            timeout = timeout
        )
    
    async def render(self, text: str) -> str:
        """Render markdown text to HTML."""
        response = await self._client.post(
            "/render",
            json = {
                "content": text
            }
        )
        return response.text