from ...context import ToolCallPacakage
from .._caller import ModelRequester
from asteval import Interpreter
from pydantic import BaseModel

@ModelRequester.reg_global_package
class Asteval(ToolCallPacakage):

    class Params(BaseModel):
        expression: str
    
    name = "asteval"
    document = "Assist in the execution of mathematical calculations."

    def call(self, args: Params):
        aeval = Interpreter()
        result = aeval(args.expression)
        return result