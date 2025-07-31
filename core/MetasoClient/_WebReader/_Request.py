from dataclasses import dataclass, asdict
from typing import Any, Dict
from environs import Env

env = Env() 

@dataclass
class RequestBody:
    """请求体对象"""
    # 问题内容
    url: str = ""

class Request:
    """请求对象"""
    url = "https://metaso.cn/api/v1/reader"
    api_key_name = ""
    body: RequestBody = RequestBody()

    @property
    def _api_key(self) -> str:
        return env.str(self.api_key_name, "")

    @property
    def headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self._api_key}',
            'Accept': 'text/plain',
            'Content-Type': 'application/json'
        }
    
    @property
    def body_dict(self) -> Dict[str, str | bool | int]:
        return asdict(self.body)
