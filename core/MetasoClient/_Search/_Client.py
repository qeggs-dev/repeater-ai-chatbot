import httpx
from ._Request import Request
from ._Response import Response

class Client:
    def __init__(self):
        self._client = httpx.AsyncClient()

    async def request(self, request: Request) -> Response:
        base_url = request.base_url
        headers = request.headers
        body = request.body_dict

        response = await self._client.post(base_url, headers=headers, json=body)
        if response.status_code == 200:
            return Response(response.json())
        else:
            response.raise_for_status()
    
    async def close(self):
        await self._client.aclose()