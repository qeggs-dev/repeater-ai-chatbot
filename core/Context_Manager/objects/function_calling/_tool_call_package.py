import orjson

from abc import ABC, abstractmethod
from typing import ClassVar, TypeVar
from pydantic import BaseModel, ValidationError
from .function import CallType
from ....User_Config_Manager import UserConfigs
from ....Global_Config_Manager import GlobalConfigs

T = TypeVar("T")

class ToolCallPacakage(ABC):
    """
    Abstract class for tool calling package
    """
    class Params(BaseModel):
        pass

    name: ClassVar[str] = ""
    enabled: ClassVar[bool] = True
    force_choice: ClassVar[bool] = False
    json_result: ClassVar[bool] = False
    call_type: ClassVar[CallType] = CallType.SYNC

    def __init__(self, user_id: str, user_configs: UserConfigs, global_configs: GlobalConfigs, *args, **kwargs):
        self.user_id = user_id
        self.user_configs = user_configs
        self.global_configs = global_configs
        self.extra_positional_args = args
        self.extra_keyword_args = kwargs

    def document(self) -> str:
        """
        Override the method to customize more complex description rules.
        """
        return self.__doc__

    @abstractmethod
    def call(self, args: Params) -> T:
        pass

    async def on_error(self, error: Exception) -> T | None:
        """
        This method is called when an error occurs during the execution of the tool.
        """
        return f"Could not call tool {self.name}: {error}"
    
    async def on_args_validation_error(self, error: ValidationError) -> T | None:
        errors = error.errors()
        buffer: list[str] = []
        for error in errors:
            buffer.append(f"{'.'.join(error['loc'])}: {error['msg']}")
        error_message = "\n".join(buffer)
        return f"Tool Args Validation Error for {self.name}:\n{error_message}"

    async def on_args_json_decode_error(self, error: orjson.JSONDecodeError) -> T | None:
        return f"Invalid JSON: {error.msg}"

    async def on_result_json_encode_error(self, error: orjson.JSONEncodeError) -> T | None:
        return f"Tool Result JSON Encode Error for {self.name}: {error}"
    
    async def on_json_result_string_encode_error(self, error: UnicodeEncodeError) -> T | None:
        return f"Tool Result JSON Can't be encoded to utf-8 string for {self.name}: {error}"