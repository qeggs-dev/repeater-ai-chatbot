# ==== 标准库 ==== #
import asyncio
import inspect
from typing import (
    Any,
    Awaitable,
    AsyncIterator
)
import time
from datetime import datetime, timezone

# ==== 第三方库 ==== #
import openai
from environs import Env
from loguru import logger

# ==== 自定义库 ==== #
from .._object import (
    Request,
    Response,
    Top_Logprob,
    Logprob,
    Delta,
    TokensCount
)
from ...Context import (
    FunctionResponseUnit,
    ContextObject,
    ContentUnit,
    ContextRole
)
from ...CallLog import CallLog
from ...CoroutinePool import CoroutinePool
from TimeParser import (
    format_deltatime,
    format_deltatime_ns
)
from .._utils import (
    remove_keys_from_dicts,
    sum_string_lengths
)
from ._process_chunk import process_chunk
from ._call_api_base import CallStreamAPIBase
from .._exceptions import *

class StreamAPI(CallStreamAPIBase):
    def __init__(self):
        self._last_response: Response | None = None

    async def call(self, user_id:str, request: Request) -> AsyncIterator[Delta]:
        """调用流式API"""
        # 创建响应对象
        model_response = Response()
        # 创建调用日志
        model_response.calling_log = CallLog()

        # 创建OpenAI Client
        logger.info(f"Created OpenAI Client", user_id = user_id)
        client = openai.AsyncOpenAI(base_url=request.url, api_key=request.key)

        # 写入调用日志基础信息
        model_response.calling_log.url = request.url
        model_response.calling_log.user_id = user_id
        model_response.calling_log.user_name = request.user_name
        model_response.calling_log.model = request.model
        model_response.calling_log.stream = request.stream

        # 如果context为空，则抛出异常
        if not request.context:
            raise ValueError("context is required")
        
        # 请求流式连接
        logger.info(f"Start Connecting to the API", user_id = user_id)
        request_start_time = time.time_ns()
        response = await client.chat.completions.create(
            model = request.model,
            temperature = request.temperature,
            top_p = request.top_p,
            frequency_penalty = request.frequency_penalty,
            presence_penalty = request.presence_penalty,
            max_tokens = request.max_tokens,
            max_completion_tokens=request.max_completion_tokens,
            stop = request.stop,
            stream = True,
            messages = remove_keys_from_dicts(request.context.full_context, {"reasoning_content"}) if not request.context.last_content.prefix else request.context.full_context,
            tools = request.function_calling.tools if request.function_calling else None,
        )
        request_end_time = time.time_ns()

        # 创建响应缓冲区单元
        model_response_content_unit:ContentUnit = ContentUnit()
        # 设置角色
        model_response_content_unit.role = ContextRole.ASSISTANT
        # chunk计数器
        chunk_count:int = 0
        # 空chunk计数器
        empty_chunk_count:int = 0

        # 开始处理流式响应
        logger.info(f"Start Streaming", user_id = user_id)
        print("\n", end="", flush=True)
        # 记录流开始时间
        stream_processing_start_time:int = time.time_ns()
        # 记录上次chunk时间
        last_chunk_time:int = 0
        # chunk耗时列表
        chunk_times:list[int] = []
        try:
            async for chunk in response:
                # 翻译chunk
                delta_data = await process_chunk(chunk)

                # 记录会话开启时间
                if not model_response.created:
                    model_response.created = delta_data.created
                
                # 记录chunk时间
                if last_chunk_time == 0:
                    last_chunk_time = delta_data.created * (10**9)
                else:
                    this_chunk_time = time.time_ns()
                    time_difference = this_chunk_time - last_chunk_time
                    chunk_times.append(time_difference)
                    last_chunk_time = this_chunk_time
                
                # 记录会话ID
                if not model_response.id:
                    model_response.id = delta_data.id
                
                # 记录模型名称
                if not model_response.model:
                    model_response.model = delta_data.model
                
                # 记录token使用情况
                if delta_data.token_usage:
                    model_response.token_usage = delta_data.token_usage

                # 记录模型推理响应内容
                if delta_data.reasoning_content:
                    if request.print_chunk:
                        if not model_response_content_unit.reasoning_content:
                            print('\n\n', end="", flush=True)
                        print(f"\033[7m{delta_data.reasoning_content}\033[0m", end="", flush=True)
                        logger.bind(donot_send_console=True).debug("Received Reasoning_Content chunk: {reasoning_content}", user_id = user_id, reasoning_content = repr(delta_data.reasoning_content))
                    model_response_content_unit.reasoning_content += delta_data.reasoning_content
                
                # 记录模型响应内容
                if delta_data.content:
                    if request.print_chunk:
                        if not model_response_content_unit.content:
                            print('\n\n', end="", flush=True)
                        print(delta_data.content, end="", flush=True)
                        logger.bind(donot_send_console=True).debug("Received Content chunk: {content}", user_id = user_id, content = repr(delta_data.content))
                    model_response_content_unit.content += delta_data.content
                
                # 记录模型工具调用内容
                if delta_data.function_id:
                    model_response_content_unit.funcResponse.callingFunctionResponse.append(
                        FunctionResponseUnit(
                            id = delta_data.function_id,
                            type = delta_data.function_type,
                            name = delta_data.function_name,
                            arguments_str = delta_data.function_arguments,
                        )
                    )
                
                if delta_data.system_fingerprint:
                    model_response.system_fingerprint = delta_data.system_fingerprint

                # 判断是否为空并增加空chunk计数器
                if delta_data.is_empty:
                    empty_chunk_count += 1
                chunk_count += 1

                # 处理回调函数
                if request.continue_processing_callback_function is not None:
                    if request.continue_processing_callback_function(user_id, delta_data):
                        break
        finally:
            # 处理结束
            stream_processing_end_time = time.time_ns()
            print('\n\n', end="", flush=True)

            # 添加日志统计数据
            model_response.calling_log.id = model_response.id
            model_response.calling_log.total_chunk = chunk_count
            model_response.calling_log.empty_chunk = empty_chunk_count
            model_response.calling_log.request_start_time = request_start_time
            model_response.calling_log.request_end_time = request_end_time
            model_response.calling_log.stream_processing_start_time = stream_processing_start_time
            model_response.calling_log.stream_processing_end_time = stream_processing_end_time
            model_response.calling_log.chunk_times = chunk_times
            model_response.calling_log.total_tokens = model_response.token_usage.total_tokens
            model_response.calling_log.prompt_tokens = model_response.token_usage.prompt_tokens
            model_response.calling_log.completion_tokens = model_response.token_usage.completion_tokens
            model_response.calling_log.cache_hit_count = model_response.token_usage.prompt_cache_hit_tokens
            model_response.calling_log.cache_miss_count = model_response.token_usage.prompt_cache_miss_tokens

            # 添加上下文
            model_response.context = request.context
            model_response.context.context_list.append(model_response_content_unit)

            # 输出响应
            self._last_response = model_response
    
    @property
    def last_response(self) -> Response | None:
        return self._last_response
