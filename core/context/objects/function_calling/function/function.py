import orjson
import asyncio
import inspect

from dataclasses import dataclass
from typing import Callable, Type, TypeVar, Any, Awaitable, Generic
from types import NoneType
from pydantic import BaseModel, ValidationError
from .call_type import CallType
from ..._tool_types import ToolTypes
from .request import (
    ToolStruct,
    FunctionStruct,
)

T = TypeVar("T")
T_BaseModel = TypeVar("T_BaseModel", BaseModel, None)

@dataclass
class Function(Generic[T, T_BaseModel]):
    """Class for function calling layer"""

    name: str = ""
    description: str = ""
    enabled: bool = True
    force_choice: bool = False
    callable: Callable[[T_BaseModel], Awaitable[T] | T] | None = None
    call_type: CallType = CallType.SYNC
    json_result: bool = False
    parameters: Type[T_BaseModel] | None = None
    on_error: Callable[[Exception], Awaitable[T | Any | None] | T | Any | None] | None = None
    on_args_validation_error: Callable[[ValidationError], Awaitable[T | Any | None] | T | Any | None] | None = None
    on_args_json_decode_error: Callable[[orjson.JSONDecodeError], Awaitable[T | Any | None] | T | Any | None] | None = None
    on_result_json_encode_error: Callable[[orjson.JSONEncodeError], Awaitable[T | Any | None] | T | Any | None] | None = None
    on_json_result_string_encode_error: Callable[[bytes, UnicodeEncodeError], Awaitable[T | Any | None] | T | Any | None] | None = None

    async def _call(self, parameters: T_BaseModel) -> T | Any | None:
        """Call the function with parameters"""
        if callable(self.callable):
            match self.call_type:
                case CallType.SYNC:
                    return self.callable(parameters)
                case CallType.ASYNC:
                    result = self.callable(parameters)
                    if inspect.isawaitable(result):
                        return await result
                    else:
                        raise RuntimeError(f"Handler is not async, Please use {CallType.SYNC} or {CallType.SYNC_IN_THREAD}")
                case CallType.SYNC_IN_THREAD:
                    return await asyncio.to_thread(self.callable, parameters)
                case _:
                    raise ValueError("Invalid call type")
        else:
            raise ValueError("Callable is not callable")

    async def call(self, parameters: T_BaseModel) -> T | Any | None:
        """Call the function"""
        try:
            return await self._call(parameters)
        except Exception as e:
            if self.on_error:
                if inspect.iscoroutinefunction(self.on_error):
                    return await self.on_error(e)
                else:
                    return self.on_error(e)
    
    def function_parameters(self) -> dict[str, Any] | None:
        """Return function parameters"""
        if self.parameters is None or self.parameters is NoneType:
            return None
        else:
            return self.parameters.model_json_schema()
    
    def struct(self, strict: bool = False) -> ToolStruct:
        """Return function struct"""
        return ToolStruct(
            type = ToolTypes.FUNCTION,
            function = FunctionStruct(
                name = self.name,
                description = self.description,
                parameters = self.function_parameters(),
                strict = strict,
            )
        )
