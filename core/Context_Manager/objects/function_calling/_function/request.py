from pydantic import BaseModel
from .._tool_types import ToolTypes
from .._value_types import ValueTypes

class FunctionParameter(BaseModel):
    type: ValueTypes = ValueTypes.STRING
    description: str = ""

class FunctionParameters(BaseModel):
    type: str = "object"
    properties: dict[str, FunctionParameter] | None = None
    required: list | None = None

class FunctionStruct(BaseModel):
    description: str = ""
    name: str = ""
    parameters: FunctionParameters | None = None
    strict: bool = False

class ToolStruct(BaseModel):
    type: ToolTypes = ToolTypes.FUNCTION
    function: FunctionStruct