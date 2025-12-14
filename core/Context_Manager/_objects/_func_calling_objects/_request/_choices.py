from enum import Enum

class RequestFunctionChoice(Enum):
    """
    FunctionCalling Request 中的选择对象
    """
    NONE = "none"
    AUTO = "auto"
    REQUIRED = "required"
    SPECIFY = "specify"