from __future__ import annotations
import json
import httpx
import socket
import asyncio
import ipaddress
from ...context_manager import ToolCallPacakage, CallType
from ...global_config_manager import HTTPMethods, ConfigManager
from .._caller import ModelRequester
from typing import Any, Self
from pydantic import BaseModel, Field

@ModelRequester.reg_global_package
class HTTPRequests(ToolCallPacakage):
    class Params(BaseModel):
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
    
    class Result(BaseModel):
        status_code: int | None = None
        reason: str = ""
        headers: dict | None = None
        cookies: dict | None = None
        data: Any = None
    
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
            if not ConfigManager.get_configs().tool_calls.allow_private_network_requests:
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
    
    name = "http_requests"
    call_type = CallType.ASYNC
    json_result = True
    client = httpx.AsyncClient(transport = PublicIPOnlyTransport())

    def document(self):
        return "send a any method HTTP request to a URL and return the response."
    
    def validation_method(self, method: HTTPMethods) -> bool:
        allowed_http_methods = self.global_configs.tool_calls.allowed_http_methods
        if allowed_http_methods is None:
            return False
        elif isinstance(allowed_http_methods, list):
            return method in allowed_http_methods
        elif allowed_http_methods == "ALL":
            return True
        else:
            return False

    async def call(self, args: Params):
        if not self.validation_method(args.method):
            return self.Result(
                reason=f"HTTP method {args.method} is not allowed."
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
        
        return self.Result(
            status_code = response.status_code,
            reason = "success",
            headers = dict(response.headers),
            cookies = dict(response.cookies),
            data = data,
        )