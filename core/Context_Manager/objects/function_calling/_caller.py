import orjson
import asyncio
from ._function import (
    Function,
    CallingRequest,
    CallType
)
from .._content_unit import ContentUnit
from .._content_role import ContentRole
from pydantic import ValidationError
from ._exceptions import JSONDecodeError, ArgumentError
from typing import Any, Callable
from ._choice import Choice
from loguru import logger

class FunctionCaller:
    def __init__(self):
        self._functions: dict[str, Function] = {}
        self._already_force_function: bool = False
    
    def to_request(self):
        return [function.struct().model_dump(exclude_none=True) for function in self._functions.values()]
    
    def to_choices(self, choice_mode: Choice = Choice.AUTO):
        match choice_mode:
            case Choice.NONE:
                return Choice.NONE.value
            case Choice.AUTO:
                return Choice.AUTO.value
            case Choice.REQUIRED:
                return Choice.REQUIRED.value
            case Choice.FORCE:
                for function in self._functions.values():
                    if function.force_choice:
                        return {
                            "type": "function",
                            "function": {
                                "name": function.name,
                            }
                        }
                raise ValueError("No function with force_choice=True found")
            case _:
                raise ValueError(f"Invalid choice mode: {choice_mode}")
    
    def check_force(self):
        for function in self._functions.values():
            if function.force_choice:
                self._already_force_function = True
                return True
        return False
    
    def register_function(self, function: Function):
        if function.force_choice:
            if self._already_force_function:
                raise ValueError("Cannot register more than one force function")
            self._already_force_function = True
        self._functions[function.name] = function
    
    def unregister_function(self, function_name: str):
        if function_name in self._functions:
            function = self._functions.pop(function_name)
            if function.force_choice:
                self._already_force_function = False
        else:
            raise ValueError(f"Function {function_name} not found")
    
    async def call_functions(self, user_id: str, calling_requests: list[tuple[CallingRequest, Callable[[Exception], ContentUnit | None] | None]], max_concurrent: int = 10) -> list[ContentUnit]:
        results: asyncio.Queue = asyncio.Queue()
        tasks: set[asyncio.Task] = set()
        semaphore = asyncio.Semaphore(max_concurrent)
        async def _call_function(user_id: str, calling_request: CallingRequest, on_error: Callable[[Exception], ContentUnit | None] | None):
            async with semaphore:
                result = await self.call_function(
                    user_id = user_id,
                    calling_request = calling_request,
                    on_error = on_error
                )
                await results.put(result)
        for request in calling_requests:
            calling_request, on_error = request
            tasks.add(
                asyncio.create_task(
                    _call_function(
                        user_id = user_id,
                        calling_request = calling_request,
                        on_error = on_error
                    )
                )
            )
        await asyncio.gather(*tasks)
        
        results_list: list[ContentUnit] = []
        while not results.empty():
            try:
                results_list.append(results.get_nowait())
            except asyncio.QueueEmpty:
                break
        
        return results_list
    
    async def call_function(self, user_id: str, calling_request: CallingRequest, on_error: Callable[[Exception], ContentUnit | None] | None = None) -> ContentUnit:
        function = self._functions[calling_request.function.name]
        parameters = function.parameters
        if parameters is not None:
            try:
                arguments = parameters(**orjson.loads(calling_request.function.arguments))
            except orjson.JSONDecodeError as e:
                raise JSONDecodeError(f"Invalid JSON: {e}") from e
            except ValidationError as e:
                errors = e.errors()
                buffer: list[str] = []
                for error in errors:
                    buffer.append(f"{'.'.join(error['loc'])}: {error['msg']}")
                raise ArgumentError("\n".join(buffer)) from e
        else:
            arguments = None
        
        
        logger.info(
            "Calling function {name}\nUse Arguments: {arguments}",
            user_id = user_id,
            name = function.name,
            arguments = arguments.model_dump_json(indent=4, ensure_ascii=False)
        )

        try:
            raw_result = await function.call(arguments)
        except Exception as e:
            if on_error is not None:
                return on_error(e)
            raise
        
        if function.json_result:
            result = orjson.dumps(raw_result)
        else:
            result = str(raw_result)
        
        return ContentUnit(
            role = ContentRole.TOOL,
            tool_call_id = calling_request.id,
            content = result
        )
    
    def __contains__(self, item: Any | Function) -> bool:
        if isinstance(item, Function):
            return item.name in self._functions
        else:
            return item in self._functions