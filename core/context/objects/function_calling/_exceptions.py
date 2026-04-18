class FunctionCallError(Exception):
    pass

class JSONDecodeError(FunctionCallError):
    pass

class ArgumentError(FunctionCallError):
    pass