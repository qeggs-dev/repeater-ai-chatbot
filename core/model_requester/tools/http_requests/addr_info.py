import httpx
import socket
import asyncio
import ipaddress
from ....global_config_manager import ConfigManager
from typing import Self
from pydantic import BaseModel

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