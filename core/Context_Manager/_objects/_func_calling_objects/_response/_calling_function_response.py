from __future__ import annotations
from dataclasses import dataclass, field
import orjson
from enum import Enum
from typing import Any
from ...._exceptions import *
from ._function_response_unit import FunctionResponseUnit

@dataclass
class CallingFunctionResponse:
    """
    FunctionCalling Response 对象
    """
    callingFunctionResponse:list[FunctionResponseUnit] = field(default_factory=list)

    def update_from_dict(self, content: list[dict]):
        other = self.from_content(content)
        self.callingFunctionResponse = other.callingFunctionResponse
    
    def to_calling_func_content(self) -> list[dict]:
        """
        模型响应对象列表
        """
        return [f.as_calling_func_unit for f in self.callingFunctionResponse]
    
    @property
    def as_calling_func_content(self) -> list[dict]:
        """
        模型响应对象列表
        """
        return self.to_calling_func_content()
    
    @classmethod
    def from_content(cls, content: list[dict]):
        """
        从模型响应对象列表中构建响应对象

        :param content: 模型响应对象列表
        :return: 响应对象
        """
        return cls(
            callingFunctionResponse = [FunctionResponseUnit.from_dict(f) for f in content]
        )
    
    def update_from_content(self, content: list[dict]):
        other = self.from_content(content)
        self.callingFunctionResponse = other.callingFunctionResponse