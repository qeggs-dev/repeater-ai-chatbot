from typing import overload, Literal, AsyncIterator
from abc import ABC, abstractmethod
from .._object import Request, Response, Delta

class BaseCallAPI(ABC):
    """
    Abstract class for calling API
    """
    @abstractmethod
    async def call(self, request: Request) -> Response | AsyncIterator[Delta]:
        pass

    @property
    @abstractmethod
    def streamable(self) -> bool:
        pass

    @property
    @abstractmethod
    def last_response(self) -> Response | None:
        pass

class CallNstreamAPIBase(BaseCallAPI, ABC):
    """
    Base class for calling non-streaming API
    """
    @property
    def streamable(self) -> Literal[False]:
        return False

    @abstractmethod
    async def call(self, request: Request) -> Response:
        pass

    @property
    @abstractmethod
    def last_response(self) -> Response | None:
        pass

class CallStreamAPIBase(BaseCallAPI, ABC):
    """
    Base class for calling streaming API
    """
    @property
    def streamable(self) -> Literal[True]:
        return True

    @abstractmethod
    async def call(self, request: Request) -> AsyncIterator[Delta]:
        pass
    
    @property
    @abstractmethod
    def last_response(self) -> Response | None:
        pass