import asyncio
from concurrent.futures import ThreadPoolExecutor
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
    executor_thread_pool: ThreadPoolExecutor | None = None

    def __post_init__(self):
        self.init_thread_pool(
            self.global_configs.tool_calls.tools_configs.asteval.max_threads
        )
    
    @classmethod
    def init_thread_pool(cls, max_workers: int):
        if cls.executor_thread_pool is not None:
            cls.executor_thread_pool = ThreadPoolExecutor(
                max_workers = max_workers
            )

    async def call(self, args: Params):
        aeval = Interpreter()
        loop = asyncio.get_event_loop()
        task = asyncio.create_task(
            loop.run_in_executor(
                self.executor_thread_pool,
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