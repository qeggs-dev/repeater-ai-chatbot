# ==== 标准库 ==== #
from typing import (
    AsyncIterator,
    Literal,
)

# ==== 第三方库 ==== #
import openai
from openai.types.chat import ChatCompletionChunk
from openai import AsyncStream
from loguru import logger

# ==== 自定义库 ==== #
from .._objects import (
    Request,
    Delta,
    Runtime
)
from ._translation_chunk import translation_chunk
from ._call_api_base import CallStreamAPIBase
from .._exceptions import *

class StreamAPI(CallStreamAPIBase):
    async def _call(self, user_id: str, request: Request, runtime: Runtime) -> AsyncIterator[Delta]:
        """
        调用流式API

        :param user_id: 用户ID
        :param request: 请求对象
        :return: 响应流
        """
        assert isinstance(user_id, str), "user_id must be a string"
        assert isinstance(request, Request), "request must be a Request object"
        assert isinstance(runtime, Runtime), "runtime must be a Runtime object"

        with runtime.status_map.enter(user_id, "Create OpenAI Client"):
            # 创建OpenAI Client
            logger.info(f"Created OpenAI Client", user_id = user_id)
            client = self.get_client(
                request = request,
                runtime = runtime
            )

        with runtime.status_map.enter(user_id, "Check context"):
            # 如果context为空，则抛出异常
            if not request.context:
                raise ValueError("context is required")
        
        with runtime.status_map.enter(user_id, "Make extra body"):
            extra_body = {}

            with runtime.status_map.enter(user_id, "thinking"):
                if request.thinking is not None:
                    if request.thinking:
                        extra_body["thinking"] = {
                            "type": "enabled"
                        }
                    else:
                        extra_body["thinking"] = {
                            "type": "disabled"
                        }
            
            with runtime.status_map.enter(user_id, "reasoning_effort"):
                if request.reasoning_effort is not None:
                    extra_body["reasoning_effort"] = request.reasoning_effort.value
        
        # 请求流式连接
        with runtime.status_map.enter(user_id, "Send Request"):
            logger.info(f"Start Connecting to the API", user_id = user_id)
            response: AsyncStream[ChatCompletionChunk] = await client.chat.completions.create(
                model = request.model,
                temperature = self.none_to_omit(request.temperature),
                top_p = self.none_to_omit(request.top_p),
                frequency_penalty = self.none_to_omit(request.frequency_penalty),
                presence_penalty = self.none_to_omit(request.presence_penalty),
                max_tokens = self.none_to_omit(request.max_tokens),
                max_completion_tokens = self.none_to_omit(request.max_completion_tokens),
                stop = self.none_to_omit(request.stop),
                stream = True,
                messages = request.context.to_context(
                    with_prompt = True,
                    remove_reasoning_prompt = request.remove_reasoning_prompt,
                    remove_created = request.remove_created,
                ),
                tools = self.none_to_omit(request.tools),
                tool_choice = self.none_to_omit(request.tool_choice),
                stream_options=request.stream_options.model_dump(),
                extra_body = extra_body
            )
        
        with runtime.status_map.enter(user_id, "Streaming"):
            async def translation_chunks(response: AsyncStream[ChatCompletionChunk]):
                logger.info("Start Streaming", user_id = user_id)
                async for chunk in response:
                    # 翻译chunk
                    delta_data = await translation_chunk(chunk)
                    yield delta_data
            
            return translation_chunks(response)