from __future__ import annotations
from typing import ClassVar

class HTTPCode:
    """
    **HTTP Status Code to Message**

    ---

    Refer to `RFC 9110` standard.

    You can read the standard document at `https://www.rfc-editor.org/rfc/rfc9110.html`.
    """
    _CODE_MAP: ClassVar[dict[int, str]] = {
        # Informational 1xx
        100: "Continue",
        101: "Switching Protocols",

        # Successful 2xx
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",

        # Redirection 3xx
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        306: "(Unused)",
        307: "Temporary Redirect",
        308: "Permanent Redirect",

        # Client Error 4xx
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Content Too Large",
        414: "URI Too Long",
        415: "Unsupported Media Type",
        416: "Range Not Satisfiable",
        417: "Expectation Failed",
        418: "(Unused)",
        421: "Misdirected Request",
        422: "Unprocessable Content",
        426: "Upgrade Required",

        # Server Error 5xx
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
    }

    def __init__(self, code: int):
        """
        :param code: HTTP Status Code
        """
        self._code = code
        self._local_map: dict[int, str] | None = None
    
    @property
    def code(self) -> int:
        """
        :return: HTTP Status Code
        """
        return self._code
    
    def expand_code_map(self, code_map: dict[int, str]) -> dict[int, str]:
        """
        **Expand the current mapping table.**

        ---

        :param code_map: Additional mapping table
        """
        if self._local_map is None:
            self._local_map = self._CODE_MAP.copy()
        self._local_map.update(code_map)
        return self._local_map
    
    @property
    def _now_map(self) -> dict[int, str]:
        """
        ## **This is an internal property and should not be accessed from outside, as it may cause abnormal internal states.**

        ---

        **Get the current mapping table.**

        ---

        :return: Mapping table
        """
        if self._local_map is not None:
            return self._local_map
        return self._CODE_MAP
    
    @classmethod
    def from_code(cls, code: int) -> HTTPCode:
        """
        **Create an instance from the HTTP Status Code.**
        
        ---

        :param code: HTTP Status Code
        """
        return cls(code)
    
    
    def code_map(self) -> dict[int, str]:
        """
        **Get the current mapping table.**
        
        ---

        :return: Mapping table
        """
        return self._now_map.copy()
    
    def __str__(self) -> str:
        """
        Get the message of the HTTP Status Code.
        """
        return self.message
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._code)})"
    
    @property
    def message(self) -> str:
        """
        **The message of the HTTP Status Code.**
        """
        return self._now_map.get(self._code, "[Undefined]")
    
    def is_valid(self) -> bool:
        """
        **Check if the HTTP Status Code is valid.**
        """
        return self._code in self._now_map
    
    @property
    def code_range(self) -> str:
        """
        **The range of the HTTP Status Code.**
        """
        if self._code in range(100, 200):
            return "Informational 1xx"
        elif self._code in range(200, 300):
            return "Successful 2xx"
        elif self._code in range(300, 400):
            return "Redirection 3xx"
        elif self._code in range(400, 500):
            return "Client Error 4xx"
        elif self._code in range(500, 600):
            return "Server Error 5xx"
        else:
            return "[Undefined]"
    
    @property
    def rfc_link(self) -> str:
        """
        **The link to the RFC document.**
        """
        url = "https://www.rfc-editor.org/rfc/rfc9110.html"
        index = f"name-{self._code}-{self.code_range.lower().replace(' ', '-')}"
        return f"{url}#{index}"
    
    def is_informational(self) -> bool:
        """
        **Check if the HTTP Status Code is informational.**
        """
        return self._code in range(100, 200)

    def is_success(self) -> bool:
        """
        **Check if the HTTP Status Code is successful.**
        """
        return self._code in range(200, 300)

    def is_redirect(self) -> bool:
        """
        **Check if the HTTP Status Code is redirect.**
        """
        return self._code in range(300, 400)

    def is_client_error(self) -> bool:
        """
        **Check if the HTTP Status Code is client error.**
        """
        return self._code in range(400, 500)

    def is_server_error(self) -> bool:
        """
        **Check if the HTTP Status Code is server error.**
        """
        return self._code in range(500, 600)