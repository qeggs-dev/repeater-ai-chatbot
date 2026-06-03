import asyncio
from ...context import ToolCallPacakage, CallType
from .._caller import ModelRequester
from asteval import Interpreter
from pydantic import BaseModel

@ModelRequester.reg_global_package
class Asteval(ToolCallPacakage):
    class Params(BaseModel):
        expression: str
        timeout: int | float | None = 5
    
    name = "asteval"
    document = "Execute Python code safely and return results."
    call_type = CallType.ASYNC

    async def call(self, args: Params):
        aeval = Interpreter()
        task = asyncio.create_task(
            asyncio.to_thread(
                aeval(
                    args.expression
                )
            )
        )
        try:
            result = await asyncio.wait_for(task, args.timeout)
        except asyncio.TimeoutError:
            task.cancel()
            return "Expression execution timed out."
        return result