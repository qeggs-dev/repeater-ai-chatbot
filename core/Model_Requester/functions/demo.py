from ...Context_Manager import ToolCallPacakage
from .._caller import ModelRequester
from pydantic import BaseModel

class Demo(ToolCallPacakage):
    
    class Params(BaseModel):
        name: str
        data: str
    
    name = "demo"
    enabled = False # Debug Only

    def document(self):
        return "Demo Tool"

    def call(self, args: Params):
        return f"Hello {args.name}, your data is {args.data}"

ModelRequester.reg_global_package(Demo)