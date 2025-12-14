from dataclasses import dataclass

@dataclass
class RequestFunctionParameters:
    """
    FunctionCalling Request 中的函数参数对象
    """
    name: str = ""
    type: str = ""
    description: str = ""
    required: bool = False