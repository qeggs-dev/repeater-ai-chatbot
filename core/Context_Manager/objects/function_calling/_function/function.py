import asyncio

from enum import Enum
from dataclasses import dataclass
from typing import Callable, Type, TypeVar, Any
from pydantic import BaseModel
from .call_type import CallType
from .._tool_types import ToolTypes
from .._value_types import ValueTypes
from .request import (
    ToolStruct,
    FunctionStruct,
    FunctionParameters,
    FunctionParameter,
)

T = TypeVar("T")
T_BaseModel = TypeVar("T_BaseModel", bound=BaseModel)

@dataclass
class Function:
    """Class for function calling layer"""

    name: str = ""
    description: str = ""
    enabled: bool = True
    force_choice: bool = False
    callable: Callable[..., T] | None = None
    call_type: CallType = CallType.SYNC
    json_result: bool = False
    parameters: Type[T_BaseModel] | None = None

    async def _call_with_param(self, parameters: T_BaseModel) -> T:
        """Call the function with parameters"""
        match self.call_type:
            case CallType.SYNC:
                return self.callable(**parameters.model_dump())
            case CallType.ASYNC:
                return await self.callable(**parameters.model_dump())
            case CallType.SYNC_IN_THREAD:
                return await asyncio.to_thread(self.callable, **parameters.model_dump())
            case _:
                raise ValueError("Invalid call type")
    
    async def _call(self) -> T:
        """Call the function"""
        match self.call_type:
            case CallType.SYNC:
                return self.callable()
            case CallType.ASYNC:
                return await self.callable()
            case CallType.SYNC_IN_THREAD:
                return await asyncio.to_thread(self.callable)
            case _:
                raise ValueError("Invalid call type")

    async def call(self, parameters: T_BaseModel | None = None) -> T:
        """Call the function"""
        if parameters is None:
            return await self._call()
        else:
            return await self._call_with_param(parameters)
    
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
