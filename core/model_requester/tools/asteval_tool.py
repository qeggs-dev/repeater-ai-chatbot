import asyncio
from typing import Any
from ...context import ToolCallPacakage, CallType
from .._caller import ModelRequester
from asteval import Interpreter
from pydantic import BaseModel, Field

@ModelRequester.reg_global_package
class Asteval(ToolCallPacakage):
    class Params(BaseModel):
        expression: str | list[str] = Field(..., description="The Python expression to evaluate. (Ban high-risk functions.)")
        symbols: dict[str, Any] | None = Field(None, description="The symbols to use in the evaluation. ")
        timeout: int | float | None = Field(5, description="The timeout for the evaluation.")
    
    name = "asteval"
    document = "Execute Python code safely and return results."
    call_type = CallType.ASYNC

    @staticmethod
    def safe_eval(
        aeval: Interpreter,
        expression: str | list[str]
    ) -> Any:
        try:
            if isinstance(expression, str):
                return aeval.eval(
                    expression,
                    raise_errors = True,
                )
            else:
                return [
                    aeval.eval(
                        expr,
                        raise_errors = True,
                    ) for expr in expression
                ]
        except Exception as e:
            return e

    async def call(self, args: Params) -> Any:
        aeval = Interpreter()

        if args.symbols:
            aeval.symtable.update(args.symbols)
        
        task = asyncio.create_task(
            asyncio.to_thread(
                self.safe_eval,
                aeval,
                args.expression
            )
        )

        try:
            result = await asyncio.wait_for(task, args.timeout)
        except asyncio.TimeoutError:
            task.cancel()
            return "Expression execution timed out."
        return result