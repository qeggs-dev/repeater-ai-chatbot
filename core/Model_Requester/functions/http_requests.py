import json
import httpx
from ...Context_Manager import ToolCallPacakage, CallType
from .._caller import ModelRequester
from typing import Any
from pydantic import BaseModel, Field
from enum import StrEnum

class HTTPMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"

@ModelRequester.reg_global_package
class HTTPRequests(ToolCallPacakage):
    client = httpx.AsyncClient()
    class Params(BaseModel):
        method: HTTPMethod = Field(HTTPMethod.GET, description="The HTTP method to use for the request.")
        url: str = Field("", description="The target URL of the request.")
        query_params: dict[str, str] | None = Field(None, description="Query parameters to append to the request URL.")
        headers: dict[str, str] | None = Field(None, description="HTTP headers to send with the request.")
        cookies: dict[str, str] | None = Field(None, description="Cookies to attach to the request.")
        form_data: dict[str, str] | None = Field(None, description="Form-data to send with the request.")
        json_data: Any | None = Field(None, description="JSON data to send in the request body.")
        auth: tuple[str, str] | None = Field(None, description="Basic authentication credentials as a (username, password) tuple.")
        follow_redirects: bool = Field(True, description="Whether to automatically follow HTTP redirects.")
        timeout_seconds: int = Field(10, description="Request timeout in seconds.")
    
    class Result(BaseModel):
        status_code: int | None = None
        reason: str = ""
        headers: dict | None = None
        cookies: dict | None = None
        data: Any = None
    
    name = "http_requests"
    call_type = CallType.ASYNC
    json_result = True

    def document(self):
        return "send a any method HTTP request to a URL and return the response."

    async def call(self, args: Params):
        if not self.global_configs.tool_calls.allow_all_http_methods:
            if args.method != HTTPMethod.GET:
                return self.Result(
                    reason = "Not allowed to use non-GET HTTP methods."
                )
        try:
            response = await self.client.request(
                args.method,
                args.url,
                params = args.query_params,
                headers = args.headers,
                cookies = args.cookies,
                data = args.form_data,
                json = args.json_data,
                auth = args.auth,
                follow_redirects = args.follow_redirects,
                timeout = args.timeout_seconds,
            )
        except httpx.Timeout:
            return self.Result(
                reason = "Timeout",
            )
        except httpx.HTTPError as e:
            return self.Result(
                reason = f"Error: {e}",
            )
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = response.text
        
        return self.Result(
            status_code = response.status_code,
            reason = "success",
            headers = dict(response.headers),
            cookies = dict(response.cookies),
            data = data,
        )