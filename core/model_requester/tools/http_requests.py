from __future__ import annotations
import json
import httpx
import socket
import asyncio
import ipaddress
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from ...context import ToolCallPacakage, CallType
from ...global_config_manager import HTTPMethods, ConfigManager
from .._caller import ModelRequester
from ...auxiliary.http import get_ssl_context
from typing import Any, Self, ClassVar
from pydantic import BaseModel, Field
from cachetools import TTLCache

class Request(BaseModel):
    method: HTTPMethods = Field(HTTPMethods.GET, description="The HTTP method to use for the request.")
    url: str = Field("", description="The target URL of the request.")
    query_params: dict[str, str] | None = Field(None, description="Query parameters to append to the request URL.")
    headers: dict[str, str] | None = Field(None, description="HTTP headers to send with the request.")
    cookies: dict[str, str] | None = Field(None, description="Cookies to attach to the request.")
    form_data: dict[str, str] | None = Field(None, description="Form-data to send with the request.")
    json_data: Any | None = Field(None, description="JSON data to send in the request body.")
    auth: tuple[str, str] | None = Field(None, description="Basic authentication credentials as a (username, password) tuple.")
    follow_redirects: bool = Field(True, description="Whether to automatically follow HTTP redirects.")
    timeout_seconds: int = Field(10, description="Request timeout in seconds.")
    verify_crawler_permissions: bool = Field(True, description="Whether to verify crawler permissions.")
    exclude_crawler_user_agent: bool = Field(False, description="Whether to not actively add the `User-Agent` in the request header (turn off this option if you need to set 'User-Agent') .")
    
class PublicIPOnlyTransport(httpx.AsyncHTTPTransport):
    class AddrInfo(BaseModel):
        family: socket.AddressFamily
        type: socket.SocketKind
        proto: int
        canonname: str
        host: str
        port: int
        flowinfo: int = 0
        scope_id: int = 0
        
        @classmethod
        def from_addr(cls, addr: tuple) -> Self:
            family, type, proto, canonname, sockaddr = addr
            
            data = {
                "family": family,
                "type": type,
                "proto": proto,
                "canonname": canonname,
                "host": sockaddr[0],
                "port": sockaddr[1],
            }
            
            if len(sockaddr) == 4:
                data["flowinfo"] = sockaddr[2]
                data["scope_id"] = sockaddr[3]
            
            return cls(**data)
        
        def to_ip_address(self) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
            return ipaddress.ip_address(self.host)
        
        @property
        def is_ipv6(self) -> bool:
            return self.family == socket.AF_INET6
        
        @property
        def address_tuple(self) -> tuple[str, int] | tuple[str, int, int, int]:
            if self.is_ipv6:
                return (self.host, self.port, self.flowinfo, self.scope_id)
            return (self.host, self.port)
    
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        if not ConfigManager.get_configs().tool_calls.tools_configs.http_requests.allow_private_network_requests:
            host = request.url.host
            port = request.url.port

            try:
                ip = ipaddress.ip_address(host)
                if ip.is_private:
                    raise httpx.TransportError("Private network requests are not allowed")
            except ValueError:
                # is not an ip address
                # try to DNS resolve
                loop = asyncio.get_event_loop()
                addrs: list[tuple[socket.AddressFamily, socket.SocketKind, int, str, tuple[str, int] | tuple[str, int, int, int]]] = await loop.getaddrinfo(
                    host,
                    port,
                    type = socket.SOCK_STREAM
                )
                for addr in addrs:
                    addr_info = self.AddrInfo.from_addr(addr)
                    if addr_info.to_ip_address().is_private:
                        raise httpx.TransportError("Private network requests are not allowed")
            
        return await super().handle_async_request(request)
    
class Response(BaseModel):
    request: Request
    status_code: int | None = None
    reason: str = ""
    headers: dict | None = None
    cookies: dict | None = None
    data: Any = None

@ModelRequester.reg_global_package
class HTTPRequests(ToolCallPacakage):

    class Params(BaseModel):
        base_url: str = Field("", description="The base URL shared by all requests.")
        base_headers: dict[str, str] | None = Field(None, description="The underlying request header shared by all requests.")
        base_cookies: dict[str, str] | None = Field(None, description="The base Cookie shared by all requests.")
        base_auth: tuple[str, str] | None = Field(None, description="The base Auth shared by all requests.")
        base_timeout: int = Field(5, description="Requests timeout in seconds.")
        requests: list[list[Request]] = Field(..., description="Sending requests in batches using connection pooling (The outer list executes sequentially, and the inner list executes in parallel.).")
    
    class Result(BaseModel):
        responses: list[list[Response]] = Field(..., description="The responses of the requests.")
    
    name = "http_requests"
    call_type = CallType.ASYNC
    json_result = True
    document = "send a any method HTTP request to a URL and return the response."
    robots_cache: ClassVar[TTLCache[str, str, float] | None] = None
    
    def validation_method(self, method: HTTPMethods) -> bool:
        allowed_http_methods = self.global_configs.tool_calls.tools_configs.http_requests.allowed_http_methods
        if allowed_http_methods is None:
            return False
        elif isinstance(allowed_http_methods, list):
            return method in allowed_http_methods
        elif allowed_http_methods == "ALL":
            return True
        else:
            return False
    
    def __post_init__(self):
        self.init_cache(
            self.global_configs.tool_calls.tools_configs.http_requests.robots_cache_size,
            self.global_configs.tool_calls.tools_configs.http_requests.robots_cache_timeout,
        )
    
    @classmethod
    def init_cache(cls, size: int, timeout: float):
        if cls.robots_cache is None:
            cls.robots_cache = TTLCache(
                maxsize = size,
                ttl = timeout
            )
    
    @staticmethod
    def get_root_url(url: str) -> str:
        parsed = urlparse(url)
        # 组合：scheme://netloc
        root = f"{parsed.scheme}://{parsed.netloc}"
        return root
    
    async def crawler_header(self) -> dict[str, str]:
        return {
            "User-Agent": self.global_configs.tool_calls.tools_configs.http_requests.crawler_name,
        }
    
    async def verify_crawler_permissions(self, client: httpx.AsyncClient, url: str) -> bool:
        base_url = self.get_root_url(client.base_url)
        raw_url = client.base_url
        if base_url != raw_url:
            client.base_url = base_url
            rewrite_url: bool = True
        else:
            rewrite_url: bool = False

        try:
            if self.robots_cache[base_url]:
                text = self.robots_cache[base_url]
            else:
                response = await client.get(
                    "/robots.txt"
                )
                if response.status_code == 200:
                    text = response.text
                    self.robots_cache[base_url] = text
                else:
                    return True

            robot_file_parser = RobotFileParser()
            robot_file_parser.parse(text.splitlines())
            return robot_file_parser.can_fetch(
                self.global_configs.tool_calls.tools_configs.http_requests.crawler_name, url
            )
        except Exception:
            return True
        finally:
            if rewrite_url: 
                client.base_url = raw_url
            
    async def send_request(self, client: httpx.AsyncClient, request: Request) -> Response:
        if not self.validation_method(request.method):
            return self.Result(
                reason=f"HTTP method {request.method} is not allowed."
            )
        
        headers = request.headers
        if not request.exclude_crawler_user_agent:
            headers.update(await self.crawler_header())
        
        if request.verify_crawler_permissions:
            if not await self.verify_crawler_permissions(client, request.url):
                return self.Result(
                    reason = "Crawler permissions denied."
                )

        try:
            response = await client.request(
                request.method,
                request.url,
                params = request.query_params,
                headers = headers,
                cookies = request.cookies,
                data = request.form_data,
                json = request.json_data,
                auth = request.auth,
                follow_redirects = request.follow_redirects,
                timeout = request.timeout_seconds,
            )
        except httpx.TimeoutException as e:
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
    
        return Response(
            request = request,
            status_code = response.status_code,
            reason = "success",
            headers = dict(response.headers),
            cookies = dict(response.cookies),
            data = data,
        )

    async def call(self, args: Params):
        client = httpx.AsyncClient(
            base_url = args.base_url,
            headers = args.base_headers,
            cookies = args.base_cookies,
            auth = args.base_auth,
            timeout = args.base_timeout,
            transport = PublicIPOnlyTransport(),
            verify = get_ssl_context()
        )

        responses: list[list[Response]] = []
        
        tasks: set[asyncio.Task[Response]] = set()
        for requests in args.requests:
            for request in requests:
                tasks.add(
                    asyncio.create_task(
                        self.send_request(
                            client,
                            request,
                        )
                    )
                )
            
            results = await asyncio.gather(*tasks)
            responses.append(results)
        
        return self.Result(
            responses = results,
        ).model_dump(exclude_none=True)