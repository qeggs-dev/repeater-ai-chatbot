import httpx
from ._Request import Request
from ._Response import Response

class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient()

    async def send_request(self, request: Request) -> Response:
        url = request.url
        headers = request.headers
        body = request.body_dict 
        response = await self.client.post(url=url, json=body, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        else:
            raise Exception(f"请求失败，状态码：{response.status_code}")
        
    async def close(self):
        await self.client.aclose()