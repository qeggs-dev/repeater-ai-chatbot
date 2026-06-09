from typing import Any
from pydantic import BaseModel
from ..auxiliary.http import HTTPCode

class HTTPErrorDetail(BaseModel):
    message: str = "Internal Server Error"
    status_code: int = 500
    extra_data: Any = None

    def http_code(self) -> HTTPCode:
        return HTTPCode(self.status_code)

class HTTPException(Exception):
    def __init__(self, detail: str = "Internal Server Error", status_code: int = 500, extra_data: Any = None):
        self.detail = HTTPErrorDetail(
            message = detail,
            status_code = status_code,
            extra_data = extra_data
        )
        super().__init__(detail)
    
    @property
    def status_code(self):
        return self.detail.status_code
    
    @property
    def message(self):
        return self.detail.message
    
    @property
    def extra_data(self):
        return self.detail.extra_data
    
    def __str__(self):
        return self.message
    
    def __repr__(self):
        return f"{self.__class__.__name__}(detail={repr(self.message)}, status_code={repr(self.status_code)}, extra_data={repr(self.extra_data)})"