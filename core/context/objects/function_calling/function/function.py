import orjson
import asyncio
import inspect

from dataclasses import dataclass
from typing import Callable, Type, TypeVar, Any, Awaitable
from types import NoneType
from pydantic import BaseModel, ValidationError
from .call_type import CallType
from ..._tool_types import ToolTypes
from .request import (
    ToolStruct,
    FunctionStruct,
)

T = TypeVar("T")
T_BaseModel = TypeVar("T_BaseModel", BaseModel, NoneType)

@dataclass
class Function:
    """Class for function calling layer"""

    name: str = ""
    description: str = ""
    enabled: bool = True
    force_choice: bool = False
    callable: Callable[[T_BaseModel], T | Awaitable[T]] | None = None
    call_type: CallType = CallType.SYNC
    json_result: bool = False
    parameters: Type[T_BaseModel] = None
    on_error: Callable[[Exception], Awaitable[T | None] | T | None] | None = None
    on_args_validation_error: Callable[[ValidationError], Awaitable[T | None] | T | None] | None = None
    on_args_json_decode_error: Callable[[orjson.JSONDecodeError], Awaitable[T | None] | T | None] | None = None
    on_result_json_encode_error: Callable[[orjson.JSONEncodeError], Awaitable[str | None] | str | None] | None = None
    on_json_result_string_encode_error: Callable[[bytes, UnicodeEncodeError], Awaitable[str | None] | str | None] | None = None

    async def _call(self, parameters: T_BaseModel) -> T:
        """Call the function with parameters"""
        match self.call_type:
            case CallType.SYNC:
                return self.callable(parameters)
            case CallType.ASYNC:
                return await self.callable(parameters)
            case CallType.SYNC_IN_THREAD:
                return await asyncio.to_thread(self.callable, parameters)
            case _:
                raise ValueError("Invalid call type")

    async def call(self, parameters: T_BaseModel | None = None) -> T:
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
        if self.parameters is None:
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
