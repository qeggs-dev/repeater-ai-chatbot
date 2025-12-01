class FunctionCallingException(Exception):
    """
    FunctionCalling异常基类
    """
    pass

class FunctionCallingArgumentsSyntaxError(FunctionCallingException):
    """
    FunctionCalling参数语法错误
    """
    pass

class FunctionNotFound(FunctionCallingException):
    """
    FunctionCalling函数未找到
    """
    pass

class FunctionArgumentsTypeError(FunctionCallingException):
    """
    FunctionCalling参数类型错误
    """
    pass

class FunctionArgumentsValueAutoTypeError(FunctionCallingException):
    """
    FunctionCalling参数值自动类型错误
    """
    pass