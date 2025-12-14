from dataclasses import dataclass, field
from ._parameters import RequestFunctionParameters

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