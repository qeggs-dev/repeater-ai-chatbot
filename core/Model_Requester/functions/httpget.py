import json
import httpx
from ...Context_Manager import ToolCallPacakage, CallType
from .._caller import ModelRequester
from pydantic import BaseModel, Field

@ModelRequester.reg_global_package
class HTTPGET(ToolCallPacakage):
    client = httpx.AsyncClient()
    class Params(BaseModel):
        url: str = Field("", description="The URL to send the GET request to")
        params: dict[str, str] | None = Field(None, description="The parameters to include in the GET request")
        headers: dict[str, str] | None = Field(None, description="The headers to include in the GET request")
        cookies: dict[str, str] | None = Field(None, description="The cookies to include in the GET request")
        auth: tuple[str, str] | None = Field(None, description="The authentication credentials to include in the GET request")
        follow_redirects: bool = Field(True, description="Whether to follow redirects")
        timeout: int = Field(10, description="The timeout for the GET request")
    
    name = "httpget"
    call_type = CallType.ASYNC
    json_result = True

    def document(self):
        return "send a GET request to a URL and return the response."

    async def call(self, args: Params):
        try:
            response = await self.client.get(
                args.url,
                params = args.params,
                headers = args.headers,
                cookies = args.cookies,
                auth = args.auth,
                follow_redirects = args.follow_redirects,
                timeout = args.timeout,
            )
        except httpx.Timeout:
            return {
                "status_code": None,
                "reason": "Timeout",
                "headers": None,
                "cookies": None,
                "data": None,
            }
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = response.text
        
        return {
            "status_code": response.status_code,
            "reason": "success",
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
            "data": data,
        }