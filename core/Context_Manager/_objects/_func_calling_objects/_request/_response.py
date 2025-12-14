from __future__ import annotations
from dataclasses import dataclass, field
from ._choices import RequestFunctionChoice
from ._function_unit import RequestCallingFunctionUnit

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