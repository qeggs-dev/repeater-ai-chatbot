import sys
import openai

from typing import Literal, AsyncIterator, TextIO, TypeVar, Any
from abc import ABC, abstractmethod
from .._objects import Request, Response, Delta, Runtime
from .._exceptions import *
from ....pools.client_pool import ClientInfo

T = TypeVar("T")

class BaseCallAPI(ABC):
    """
    Abstract class for calling API
    """
    def __init__(self, print_file: TextIO = sys.stdout):
        self._print_file = print_file
    
    @staticmethod
    def get_client(request: Request, runtime: Runtime) -> openai.AsyncClient:
        client_info = ClientInfo(
            url = request.url,
            proxy = request.proxy,
            encoding = request.encoding,
            timeout = request.timeout
        )
        client = runtime.client_pool.get_openai(
            client_info = client_info,
            api_key = request.key
        )
        return client
    
    @staticmethod
    def none_to_omit(value: Any) -> Any:
        if value is None:
            return openai.omit
        return value

    async def call(self, user_id: str, request: Request, runtime: Runtime) -> T:
        """
        调用API

        :param user_id: 用户ID
        :param request: 请求对象
        :return: 响应对象
        """
        if user_id is None:
            raise ValueError("user_id cannot be None")
        if not isinstance(request, Request):
            raise TypeError("request must be Request")
        if not isinstance(runtime, Runtime):
            raise TypeError("runtime must be Runtime")
        
        try:
            return await self._call(user_id, request, runtime)
        except openai.APITimeoutError as e:
            raise APITimeoutError(str(e)) from e
        except openai.BadRequestError as e:
            raise BadRequestError(str(e)) from e
        except openai.InternalServerError as e:
            raise APIServerError(str(e)) from e
        except openai.APIConnectionError as e:
            raise APIConnectionError(str(e)) from e
        except Exception as e:
            raise CallAPIException(str(e)) from e
    
    @abstractmethod
    async def _call(self, user_id: str, request: Request, runtime: Runtime) -> T:
        pass

    @property
    @abstractmethod
    def streamable(self) -> bool:
        pass

class CallNstreamAPIBase(BaseCallAPI, ABC):
    """
    Base class for calling non-streaming API
    """

    @property
    def streamable(self) -> Literal[False]:
        return False

    @abstractmethod
    async def _call(self, user_id: str, request: Request, runtime: Runtime) -> Response:
        pass

class CallStreamAPIBase(BaseCallAPI, ABC):
    """
    Base class for calling streaming API
    """

    @property
    def streamable(self) -> Literal[True]:
        return True

    @abstractmethod
    async def _call(self, user_id: str, request: Request, runtime: Runtime) -> AsyncIterator[Delta]:
        pass