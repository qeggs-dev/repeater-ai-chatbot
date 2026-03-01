# ==== 标准库 ==== #
from typing import (
    AsyncIterator,
    Literal,
)

# ==== 第三方库 ==== #
import openai
from openai.types.chat import ChatCompletionChunk
from openai import NOT_GIVEN, AsyncStream
from loguru import logger

# ==== 自定义库 ==== #
from .._objects import (
    Request,
    Delta,
)
from ._translation_chunk import translation_chunk
from ._call_api_base import CallStreamAPIBase
from .._exceptions import *
from ....Status_Map import StatusMap

class StreamAPI(CallStreamAPIBase):
    async def _call(self, user_id: str, request: Request, status_map: StatusMap[str, str]) -> AsyncIterator[Delta]:
        """
        调用流式API

        :param user_id: 用户ID
        :param request: 请求对象
        :return: 响应流
        """
        assert isinstance(user_id, str), "user_id must be a string"
        assert isinstance(request, Request), "request must be a Request object"

        with status_map.enter(user_id, "Create OpenAI Client"):
            # 创建OpenAI Client
            logger.info(f"Created OpenAI Client", user_id = user_id)
            client = openai.AsyncOpenAI(
                base_url = request.url,
                api_key = request.key,
                timeout = request.timeout,
            )

        with status_map.enter(user_id, "Check context"):
            # 如果context为空，则抛出异常
            if not request.context:
                raise ValueError("context is required")
        
        with status_map.enter(user_id, "Make extra body"):
            extra_body = {}

            with status_map.enter(user_id, "thinking"):
                if request.thinking is not None:
                    if request.thinking:
                        extra_body["thinking"] = {
                            "type": "enabled"
                        }
                    else:
                        extra_body["thinking"] = {
                            "type": "disabled"
                        }
        
        # 请求流式连接
        with status_map.enter(user_id, "Send Request"):
            logger.info(f"Start Connecting to the API", user_id = user_id)
            response: AsyncStream[ChatCompletionChunk] = await client.chat.completions.create(
                model = request.model,
                temperature = request.temperature,
                top_p = request.top_p,
                frequency_penalty = request.frequency_penalty,
                presence_penalty = request.presence_penalty,
                max_tokens = request.max_tokens,
                max_completion_tokens=request.max_completion_tokens,
                stop = request.stop,
                stream = True,
                messages = request.context.to_full_context(remove_resoning_prompt=True),
                tools = request.function_calling.tools if request.function_calling else None,
                stream_options=request.stream_options.model_dump(),
                extra_body = extra_body
            )
        
        class Generator_Warp:
            def __init__(self, generator: AsyncStream[ChatCompletionChunk]):
                self.generator = generator
                self._is_done = False

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self._is_done:
                    raise StopAsyncIteration
                try:
                    with status_map.enter(user_id, "Waiting chunk"):
                        chunk = await self.generator.__anext__()
                    return chunk
                except StopAsyncIteration:
                    self._is_done = True
                    raise
                

        with status_map.enter(user_id, "Streaming"):
            logger.info("Start Streaming", user_id = user_id)
            async for chunk in Generator_Warp(response):
                # 翻译chunk
                with status_map.enter(user_id, "Translation Chunk"):
                    delta_data = await translation_chunk(chunk)
                yield delta_data