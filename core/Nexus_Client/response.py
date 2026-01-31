from httpx import Response
from typing import (
    TypeVar,
    Generic,
    Type,
    Any
)
from pydantic import BaseModel, ValidationError
from loguru import logger

T = TypeVar("T", bound = BaseModel)

class NexusResponse(Generic[T]):
    """Nexus Response Model"""
    def __init__(
            self,
            response: Response,
            model: Type[T] | None = None
        ) -> None:
        self._response = response
        self._model = model
    
    @property
    def code(self) -> int:
        return self._response.status_code
    
    @property
    def content(self) -> str:
        return self._response.text
    
    @property
    def json(self) -> Any:
        return self._response.json()
    
    def data(self) -> T | None:
        if self._model is None:
            raise ValueError("Model is not set")
        try:
            return self._model(
                **self._response.json()
            )
        except ValidationError as e:
            errors = e.errors()
            for error in errors:
                logger.error(
                    "{field}: {message}",
                    field = ".".join(error["loc"]),
                    message = error["msg"]
                )
            return None
