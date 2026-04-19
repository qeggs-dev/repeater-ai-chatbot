import asyncio

from ..context import (
    Function,
    FunctionCaller,
    CallingRequest,
    Context,
    ContentUnit,
    ToolChoice,
    ToolCallPacakage
)
from ..call_api.completions_api import (
    StreamClient,
    NoStreamClient,
    Request,
    Response,
    Delta
)
from ..text_buffer import ContentBuffer
from ..status_map import StatusMap
from ..user_config_manager import UserConfigs
from ..global_config_manager import ConfigManager
from typing import (
    AsyncGenerator,
    ClassVar,
    Type
)
from loguru import logger
from ._exceptions import *
from ._multi_response import MultiResponse

class ModelRequester:
    _global_package: ClassVar[list[Type[ToolCallPacakage]]] = []
    def __init__(self, user_id: str, user_configs: UserConfigs, max_concurrency: int | None = None, *args, **kwargs):
        self._tools_caller = FunctionCaller()
        self._tools_caller.register_packages(
            user_id = user_id,
            packages = self._global_package,
            user_configs = user_configs,
            *args,
            **kwargs
        )
        self._api_client = NoStreamClient(
            ConfigManager.get_configs().callapi.max_concurrency
            if max_concurrency is None else max_concurrency
        )
        self._stream_api_client = StreamClient(
            ConfigManager.get_configs().callapi.max_concurrency
            if max_concurrency is None else max_concurrency
        )
        self._stream_chunk_queue: asyncio.Queue[Delta | ContentUnit | None] = asyncio.Queue()
        self._tool_responses: list[list[ContentUnit]] = []
    
    @classmethod
    def reg_global_package(cls, package: Type[ToolCallPacakage]):
        if not issubclass(package, ToolCallPacakage):
            raise TypeError("package must be a subclass of ToolCallPacakage")
        cls._global_package.append(package)
        return package
    
    def reg_func(self, function: Function):
        self._tools_caller.register_function(function)
    
    def reg_packages(self, user_id: str, packages: list[Type[ToolCallPacakage]], user_configs: UserConfigs):
        self._tools_caller.register_packages(
            user_id = user_id,
            packages = packages,
            user_configs = user_configs
        )
    
    def unreg_func(self, func_name: str):
        self._tools_caller.unregister_function(func_name)
    
    @property
    def tools_caller(self) -> FunctionCaller:
        return self._tools_caller
    
    @tools_caller.setter
    def tools_caller(self, tools_caller: FunctionCaller):
        if not isinstance(tools_caller, FunctionCaller):
            raise TypeError("tools_caller must be a FunctionCaller")
        self._tools_caller = tools_caller
    
    async def generator(self) -> AsyncGenerator[Delta | ContentUnit, None]:
        failed_times: int = 0
        while True:
            try:
                delta = await asyncio.wait_for(self._stream_chunk_queue.get(), 10)
            except asyncio.TimeoutError:
                failed_times += 1
                if failed_times > 5:
                    break
            if delta is None:
                break
            yield delta
    
    async def _parse_response(self, request: Request, response: Response) -> Response:
        if response.tool_calls:
            calling_requests: list[CallingRequest] = []
            for tool_call in response.tool_calls:
                calling_requests.append(tool_call.to_calling_request())
            results = await self._tools_caller.call_functions(
                response.user_id,
                calling_requests = calling_requests
            )
            self._tool_responses.append(results)
            for tool_response in results:
                await self._stream_chunk_queue.put(tool_response)
            if request.context:
                request.context.extend(response.new_context)
                request.context.extend(results)
            else:
                request.context = Context(
                    context_list = results
                )
            if request.thinking:
                request.remove_reasoning_prompt = False
            raise Regenerate(request)
    
    async def submit(
        self,
        user_id:str,
        request: Request,
        content_buffer: ContentBuffer,
        status_map: StatusMap[str, str],
        allow_tool_calls: bool = True,
        tool_choice_model: ToolChoice = ToolChoice.AUTO,
        stream: bool = False,
    ) -> MultiResponse:
        generated_times: int = 0
        max_generated_times: int = ConfigManager.get_configs().callapi.max_regenerate_times
        responses: MultiResponse = MultiResponse()
        responses.historical_context = request.context
        submit_context = request.context.remove_reasoning_content()
        request.context = submit_context
        if allow_tool_calls and max_generated_times > 1:
            request.tools = self._tools_caller.to_request()
            request.tool_choice = self._tools_caller.to_choice(tool_choice_model)
        try:
            while True:
                try:
                    generated_times += 1
                    logger.info(
                        "Generate Times: {now}/{max}",
                        user_id = user_id,
                        now = generated_times,
                        max = max_generated_times
                    )
                    if stream:
                        async def send_chunk(delta: Delta):
                            await self._stream_chunk_queue.put(delta)
                        response = await self._stream_api_client.submit_request(
                            user_id = user_id,
                            request = request,
                            content_buffer = content_buffer,
                            status_map = status_map,
                            chunk_callback = send_chunk
                        )
                    else:
                        response = await self._api_client.submit_request(
                            user_id = user_id,
                            request = request,
                            content_buffer = content_buffer,
                            status_map = status_map
                        )
                    responses.add(response)
                    responses.tool_requests = self._tool_responses
                    await self._parse_response(
                        request = request,
                        response = response
                    )
                    raise GenerateFinished
                except Regenerate as e:
                    logger.info(
                        "Regenerate",
                        user_id = user_id,
                    )
                    request = e.request
                    content_buffer.clear()
                    if generated_times >= max_generated_times:
                        raise GenerateFinished
                    elif (generated_times + 1) >= max_generated_times:
                        logger.warning(
                            "Times too many, removeing tools",
                            user_id = user_id,
                        )
                        request.tools = None
                        request.tool_choice = None
        except GenerateFinished as e:
            logger.info(
                "GenerateFinished",
                user_id = user_id,
            )
            content_buffer.clear()
            return responses
                