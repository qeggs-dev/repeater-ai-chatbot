import httpx

from yarl import URL

class StaticResourcesClient:
    def __init__(self, base_url: str, timeout: int | float | None = None):
        if isinstance(base_url, str):
            if base_url:
                self.base_url = base_url
            else:
                raise ValueError("base_url cannot be empty")
        else:
            raise TypeError("base_url must be a string")
        
        self.client = httpx.AsyncClient(
            base_url = self.base_url,
            timeout = timeout,
        )
    
    def str_or_url(self, path: str | URL) -> str:
        if isinstance(path, str):
            return path
        elif isinstance(path, URL):
            return str(path)
        else:
            raise TypeError("path must be a string or URL")
    
    async def get_file(self, path: str | URL) -> bytes:
        """Get a file from the server."""
        response = await self.client.get(
            self.str_or_url(path)
        )
        response.raise_for_status()
        return response.content
    
    async def get_text(self, path: str | URL, text_encoding: str = "utf-8") -> str:
        """Get a text file from the server."""
        response = await self.client.get(
            self.str_or_url(path),
            params = {
                "text_encoding": text_encoding,
            }
        )
        response.raise_for_status()
        return response.text
    
    async def close(self):
        await self.client.aclose()