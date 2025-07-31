from dataclasses import dataclass

@dataclass
class Response:
    """响应对象"""
    source_url: str = ""
    content: str = ""