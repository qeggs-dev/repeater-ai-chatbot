import sys
from typing import overload, Literal, AsyncIterator, TextIO, TypeVar
from abc import ABC, abstractmethod
from .._objects import Request, Response, Delta
from .._exceptions import *
import openai

T = TypeVar("T")

class BaseCallAPI(ABC):
    """
    Abstract class for calling API
    """
    def __init__(self, print_file: TextIO = sys.stdout):
        self._print_file = print_file

    def call(self, user_id: str, request: Request) -> T:
        """
        调用API

        :param user_id: 用户ID
        :param request: 请求对象
        :return: 响应对象
        """
        try:
            return self._call(user_id, request)
        except openai.APITimeoutError as e:
            raise APITimeoutError(str(e)) from e
        except openai.BadRequestError as e:
            raise BadRequestError(str(e)) from e
        except openai.InternalServerError as e:
            raise APIServerError(str(e)) from e
        except openai.APIConnectionError as e:
            raise APIConnectionError(str(e)) from e
        except Exception as e:
            raise CallApiException(str(e)) from e
    
    @abstractmethod
    def _call(self, user_id: str, request: Request) -> T:
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
    async def _call(self, user_id: str, request: Request) -> Response:
        pass

class CallStreamAPIBase(BaseCallAPI, ABC):
    """
    Base class for calling streaming API
    """

    @property
    def streamable(self) -> Literal[True]:
        return True

    @abstractmethod
    async def _call(self, user_id: str, request: Request) -> AsyncIterator[Delta]:
        pass