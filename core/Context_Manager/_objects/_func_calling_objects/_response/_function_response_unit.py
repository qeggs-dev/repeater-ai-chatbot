from __future__ import annotations
from dataclasses import dataclass
import orjson
from typing import Any
from ...._exceptions import *

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