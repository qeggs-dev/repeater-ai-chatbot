from __future__ import annotations
from dataclasses import dataclass, field
import orjson
from enum import Enum
from typing import Any
from ._exceptions import *

@dataclass
class RequestFunctionParameters:
    """
    FunctionCalling Request 中的函数参数对象
    """
    name: str = ""
    type: str = ""
    description: str = ""
    required: bool = False

@dataclass
class RequestCallingFunctionUnit:
    """
    FunctionCalling Request 中的函数对象单元
    """
    name: str = ""
    description: str = ""
    parameters: list[RequestFunctionParameters] = field(default_factory=list)

    @property
    def as_calling_func_struct(self) -> dict:
        """
        获取函数对象字典
        """
        properties = {}
        required = []
        for param in self.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description
            }
            if param.required:
                required.append(param.name)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

class RequestFunctionChoice(Enum):
    """
    FunctionCalling Request 中的选择对象
    """
    NONE = "none"
    AUTO = "auto"
    REQUIRED = "required"
    SPECIFY = "specify"


@dataclass
class CallingFunctionRequest:
    """
    FunctionCalling Request对象
    """
    functions: list[RequestCallingFunctionUnit] = field(default_factory=list)
    func_choice: RequestFunctionChoice | None = None
    func_choice_name: str | None = None

    @property
    def as_tool_choice(self) -> str | dict | None:
        """
        tool_choice字段值
        """
        if self.func_choice == RequestFunctionChoice.SPECIFY:
            return {
                "type": "function",
                "function": {
                    "name": self.func_choice_name
                }
            }
        else:
            return self.func_choice.value
    
    @property
    def tools(self) -> list[dict]:
        return [f.as_calling_func_struct() for f in self.functions]

@dataclass
class FunctionResponseUnit:
    """
    FunctionCalling Response 对象单元
    """
    id: str = ""
    type: str = ""
    name: str = ""
    arguments_str: str = ""
    
    def load_arguments(self) -> Any:
        """
        从模型输出的参数字符串中解析出对象

        :raise ContextSyntaxError: 参数字符串格式错误
        """
        try:
            return orjson.loads(self.arguments_str)
        except orjson.JSONDecodeError:
            raise ContextSyntaxError("Invalid JSON format in function response arguments.")
    
    def to_calling_func_unit(self) -> dict:
        """
        OpenAI兼容的FunctionCalling响应对象单元格式
        """
        return {
            "id": self.id,
            "type": self.type,
            "function":{
                "name": self.name,
                "arguments": self.load_arguments()
            }
        }
    
    @property
    def as_calling_func_unit(self) -> dict:
        """
        OpenAI兼容的FunctionCalling响应对象单元格式
        """
        return self.to_calling_func_unit()
    
    @classmethod
    def from_dict(cls, data: dict) -> FunctionResponseUnit:
        """
        从字典创建对象

        :param data: OpenAI兼容的FunctionCalling响应对象单元格式
        """
        # 处理id字段
        if "id" not in data:
            raise ContextNecessaryFieldsMissingError("\"id\" is a necessary field.")
        elif not isinstance(data["id"], str):
            raise ContextFieldTypeError("\"id\" must be a string.")
        else:
            id = data["id"]
        
        # 处理type字段
        if "type" not in data:
            raise ContextNecessaryFieldsMissingError("\"type\" is a necessary field.")
        elif not isinstance(data["type"], str):
            raise ContextFieldTypeError("\"type\" must be a string.")
        else:
            type = data["type"]
        
        # 处理function字段
        if "function" not in data:
            raise ContextNecessaryFieldsMissingError("\"function\" is a necessary field")
        elif not isinstance(data["function"], dict):
            raise ContextFieldTypeError("\"function\" must be a dictionary.")
        else:
            # 处理function.name字段
            if "name" not in data["function"]:
                raise ContextNecessaryFieldsMissingError("\"function.name\" is a necessary field")
            elif not isinstance(data["function"]["name"], str):
                raise ContextFieldTypeError("\"function.name\" must be a string")
            else:
                name = data["function"]["name"]
            
            # 处理function.arguments字段
            if "arguments" not in data["function"]:
                raise ContextNecessaryFieldsMissingError("\"function.arguments\" is a necessary field")
            elif not isinstance(data["function"]["arguments"], str):
                raise ContextFieldTypeError("\"function.arguments\" must be a string")
            else:
                arguments_str = data["function"]["arguments"]
        
        # 返回对象
        return cls(
            id = id,
            type = type,
            name = name,
            arguments_str = arguments_str
        )
    
    def update_from_dict(self, data: dict) -> None:
        other = self.from_dict(data)
        self.id = other.id
        self.type = other.type
        self.name = other.name
        self.arguments_str = other.arguments_str

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