from ...context import ToolCallPacakage
from .._caller import ModelRequester
from asteval import Interpreter
from pydantic import BaseModel

@ModelRequester.reg_global_package
class Asteval(ToolCallPacakage):
    aeval = Interpreter()

    class Params(BaseModel):
        expression: str
    
    name = "asteval"

    def document(self):
        return "Assist in the execution of mathematical calculations."

    def call(self, args: Params):
        result = self.aeval.parse(args.expression)
        return result