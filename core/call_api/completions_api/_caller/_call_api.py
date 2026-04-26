# ==== 标准库 ==== #
from datetime import datetime

# ==== 第三方库 ==== #
import openai
from openai.types.chat import ChatCompletion
from openai import NOT_GIVEN
from loguru import logger

# ==== 自定义库 ==== #
from .._objects import (
    Request,
    Response,
    ToolCall,
    TopLogprob,
    Logprob,
    TokensCount,
    FinishReason,
    Runtime
)
from ....context import (
    ContentUnit,
    ContentRole
)
from ....request_log import RequestLog, TimeStamp
from ._call_api_base import CallNstreamAPIBase
from ....status_map import StatusMap
from .._exceptions import *
from ....runtime_container import ClientInfo, RuntimeContainer

class CallAPI(CallNstreamAPIBase):
    async def _call(self, user_id:str, request: Request, runtime: Runtime) -> Response:
        """调用API"""
        # 检查参数
        assert isinstance(user_id, str), "user_id must be str"
        assert isinstance(request, Request), "request must be Request"
        assert isinstance(runtime, Runtime), "runtime must be Runtime"

        with runtime.status_map.enter(user_id, "Init objects"):
            # 创建模型响应对象
            model_response = runtime.response
            # 设置 user_id
            model_response.user_id = user_id
            # 创建调用日志对象
            model_response.request_log = RequestLog()

        with runtime.status_map.enter(user_id, "Create OpenAI Client"):
            # 创建OpenAI Client
            logger.info(f"Created OpenAI Client", user_id = user_id)
            client_info = ClientInfo(
                url = request.url,
                key = request.key,
                timeout = request.timeout
            )
            client = RuntimeContainer.get_runtime().openai_pool.get_client(client_info)
        
        with runtime.status_map.enter(user_id, "Write calling log base data"):
            # 写入调用日志基础数据
            model_response.request_log.url = request.url
            model_response.request_log.user_id = user_id
            model_response.request_log.user_name = request.user_name
            model_response.request_log.model = request.model
            model_response.request_log.stream = request.stream

        # 如果上下文为空，则抛出异常
        with runtime.status_map.enter(user_id, "Check context"):
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
        
        # 发送请求
        with runtime.status_map.enter(user_id, "Send Request"):
            logger.info(f"Send Request", user_id = user_id)
            request_start_time = TimeStamp()
            response: ChatCompletion = await client.chat.completions.create(
                model = request.model,
                temperature = request.temperature,
                top_p = request.top_p,
                frequency_penalty = request.frequency_penalty,
                presence_penalty = request.presence_penalty,
                max_tokens = request.max_tokens,
                max_completion_tokens=request.max_completion_tokens,
                stop = request.stop,
                stream = False,
                messages = request.context.to_context(
                    with_prompt = True,
                    remove_reasoning_prompt = request.remove_reasoning_prompt,
                    remove_created = request.remove_created,
                ),
                tools = request.tools,
                tool_choice = request.tool_choice,
                stream_options = request.stream_options.model_dump(),
                extra_body = extra_body
            )
            request_end_time = TimeStamp()

        with runtime.status_map.enter(user_id, "Processing Response"):
            # 创建响应内容单元
            model_response_content_unit:ContentUnit = ContentUnit()
            # 设置角色
            model_response_content_unit.role = request.output_role
            # chunk计数
            chunk_count:int = 0
            # 空chunk计数
            empty_chunk_count:int = 0
            self._print_file.write("\n")
            self._print_file.flush()

            # 处理响应基础信息
            if hasattr(response, "id"):
                model_response.id = response.id
            
            # 写入响应创建时间
            if hasattr(response, "created"):
                model_response.created = response.created
            
            # 写入模型名称
            if hasattr(response, "model"):
                model_response.model = response.model
            
            # 写入系统指纹
            if hasattr(response, "system_fingerprint"):
                model_response.system_fingerprint = response.system_fingerprint
            
            # 处理响应内容
            if hasattr(response, "choices"):
                choices = response.choices[0]
                # 写入完成原因
                if hasattr(choices, "finish_reason"):
                    model_response.finish_reason = FinishReason(choices.finish_reason)
                # 
                if hasattr(choices, "message"):
                    # 处理推理内容
                    if hasattr(choices.message, "reasoning_content"):
                        model_response_content_unit.reasoning_content = choices.message.reasoning_content
                        self._print_file.write(f"\n\n\033[7m{model_response_content_unit.reasoning_content}\033[0m")
                        self._print_file.flush()
                    
                    # 处理输出内容
                    if hasattr(choices.message, "content"):
                        model_response_content_unit.content = choices.message.content
                        self._print_file.write(f"\n\n{model_response_content_unit.content}\n\n")
                        self._print_file.flush()
                    
                    # 处理工具调用
                    if hasattr(choices.message, "tool_calls") and choices.message.tool_calls is not None:
                        for call in choices.message.tool_calls:
                            tool_call = ToolCall()
                            # 处理调用函数
                            if hasattr(call, "id"):
                                tool_call.id = call.id
                            if hasattr(call, "type"):
                                tool_call.type = call.type
                            if hasattr(call, "function"):
                                if hasattr(call.function, "name"):
                                    tool_call.name = call.function.name
                                if hasattr(call.function, "arguments"):
                                    tool_call.arguments = call.function.arguments
                                    self._print_file.write(f"\n\n\033[104m{tool_call.arguments}\033[0m\n\n")
                                    self._print_file.flush()
                            model_response.tool_calls.append(tool_call)
            
            # 处理logprobs
            if hasattr(response.choices, "logprobs"):
                if hasattr(response.choices.logprobs, "content"):
                    logprobs = []
                    for token in response.choices.logprobs.content:
                        logprob = Logprob()
                        if hasattr(token, "token"):
                            logprob.token = token.token
                        if hasattr(token, "logprob"):
                            logprob.logprob = token.logprob
                        if hasattr(token, "top_logprob"):
                            top_logprobs = []
                            for top_token in token.top_logprob:
                                top_logprob = TopLogprob()
                                if hasattr(top_token, "token"):
                                    top_logprob.token = top_token.token
                                if hasattr(top_token, "logprob"):
                                    top_logprob.logprob = top_token.logprob
                                top_logprobs.append(top_logprob)
                            logprob.top_logprobs = top_logprobs
                        logprobs.append(logprob)
                    logprobs = logprobs
            
            # 处理usage数据
            model_response.token_usage = TokensCount()
            if hasattr(response, "usage") and response.usage is not None:
                if hasattr(response.usage, "prompt_tokens") and response.usage.prompt_tokens is not None:
                    model_response.token_usage.prompt_tokens = response.usage.prompt_tokens
                if hasattr(response.usage, "completion_tokens") and response.usage.completion_tokens is not None:
                    model_response.token_usage.completion_tokens = response.usage.completion_tokens
                if hasattr(response.usage, "total_tokens") and response.usage.total_tokens is not None:
                    model_response.token_usage.total_tokens = response.usage.total_tokens
                if hasattr(response.usage, "prompt_cache_hit_tokens") and response.usage.prompt_cache_hit_tokens is not None:
                    model_response.token_usage.prompt_cache_hit_tokens = response.usage.prompt_cache_hit_tokens
                if hasattr(response.usage, "prompt_cache_miss_tokens") and response.usage.prompt_cache_miss_tokens is not None:
                    model_response.token_usage.prompt_cache_miss_tokens = response.usage.prompt_cache_miss_tokens

            self._print_file.write("\n\n")

            # 添加日志统计数据
            model_response.request_log.id = model_response.id
            model_response.request_log.total_chunk = chunk_count
            model_response.request_log.empty_chunk = empty_chunk_count
            model_response.request_log.request_start_time = request_start_time
            model_response.request_log.request_end_time = request_end_time
            model_response.request_log.total_tokens = model_response.token_usage.total_tokens
            model_response.request_log.prompt_tokens = model_response.token_usage.prompt_tokens
            model_response.request_log.completion_tokens = model_response.token_usage.completion_tokens
            model_response.request_log.cache_hit_count = model_response.token_usage.prompt_cache_hit_tokens
            model_response.request_log.cache_miss_count = model_response.token_usage.prompt_cache_miss_tokens

            # 添加上下文
            model_response.historical_context = request.context
            model_response.new_context.append(model_response_content_unit)

            return model_response