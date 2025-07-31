from dataclasses import dataclass, asdict
from typing import Any, Dict, Literal
from environs import Env

env = Env()

@dataclass
class RequestBody:
    """请求体对象"""
    # 问题内容
    q: str = ""
    # 搜索范围
    scope:Literal["webpage", "document", "scholar", "image", "video", "podcast"] = "webpage"
    # 内容召回增强
    includeSummary: bool = True
    # 结果数量
    size: int = 10
    # 抓取原文
    includeRawContent: bool = False
    # 精简原文匹配信息
    conciseSnippet: bool = False

class Request:
    """请求对象"""
    base_url = "https://metaso.cn/api/v1/search"
    api_key_name = ""
    _custom_apikey = ""
    body: RequestBody = RequestBody()

    @property
    def api_key(self) -> str:
        if self._custom_apikey:
            return self._custom_apikey  
        return env.str(self.api_key_name, "")
    
    @api_key.setter
    def api_key(self, api_key: str):
        self._custom_apikey = api_key

    @property
    def headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    @property
    def body_dict(self) -> Dict[str, str | bool | int]:
        return asdict(self.body)
