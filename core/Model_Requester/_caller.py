import asyncio

from ..Context_Manager import (
    Function,
    FunctionCaller,
    CallingRequest,
    ContextObject,
    ContentUnit,
    ToolChoice,
    ToolCallPacakage
)
from ..CallAPI.CompletionsAPI import (
    StreamClient,
    NoStreamClient,
    Request,
    Response,
    Delta
)
from ..TextBuffer import ContentBuffer
from ..Status_Map import StatusMap
from ..User_Config_Manager import UserConfigs
from ..Global_Config_Manager import ConfigManager
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
    def __init__(self, user_id: str, user_configs: UserConfigs, max_concurrency: int | None = None):
        self._tools_caller = FunctionCaller()
        self._tools_caller.register_packages(
            user_id = user_id,
            packages = self._global_package,
            user_configs = user_configs
        )
        self._api_client = NoStreamClient(
            ConfigManager.get_configs().callapi.max_concurrency
            if max_concurrency is None else max_concurrency
        )
        self._stream_api_client = StreamClient(
            ConfigManager.get_configs().callapi.max_concurrency
            if max_concurrency is None else max_concurrency
        )
        self._stream_chunk_queue: asyncio.Queue[Delta | None] = asyncio.Queue()
        self._tool_responses: list[list[ContentUnit]] = []
    
    @classmethod
    def reg_global_package(cls, package: Type[ToolCallPacakage]):
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
    
    async def generator(self) -> AsyncGenerator[Delta, None]:
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
            if request.context:
                request.context.extend(response.new_context)
                request.context.extend(results)
            else:
                request.context = ContextObject(
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
        responses: MultiResponse = MultiResponse()
        responses.historical_context = request.context
        submit_context = request.context.remove_reasoning_content()
        request.context = submit_context
        if allow_tool_calls:
            request.tools = self._tools_caller.to_request()
            request.tool_choice = self._tools_caller.to_choice(tool_choice_model)
        while True:
            try:
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
                return responses
            except Regenerate as e:
                logger.info(
                    "Regenerate",
                    user_id = user_id,
                )
                request = e.request
                
