# ==== 标准库 ==== #
import random
import atexit
import asyncio
import traceback
from pathlib import Path
from typing import (
    AsyncIterator,
    Any,
)

# ==== 第三方库 ==== #
import orjson
import aiofiles
from loguru import logger

# ==== 自定义库 ==== #
from ..call_api.completions_api import (
    Request,
)
from ..context import (
    ContentRole,
    Context,
    ContentUnit,
)
from ..user_config_manager import (
    UserConfigs
)
from ..global_config_manager import GlobalConfigs
from ..assist_struct import (
    RequestUserInfo,
)
from ..clients.model_info import (
    ModelInfo,
)
from ..special_exception import HTTPException
from ._print_request_info import print_request_info

def make_request(
    user_id: str,
    user_input: ContentUnit,
    user_info: RequestUserInfo,
    submit_context: Context,
    model: ModelInfo,
    configs: UserConfigs,
    global_configs: GlobalConfigs,
    assistant_role: ContentRole,
    role_name: str | None = None,
    thinking: bool | None = None
) -> Request:
    # 创建请求对象
    request = Request()
    # 设置上下文
    request.context = submit_context
    
    # 设置请求对象的API信息
    request.url = model.url
    request.model = model.id
    request.limits = model.limits
    request.timeout = model.timeout
    if configs.model_timeout is None:
        request.timeout = model.timeout
    else:
        request.timeout = configs.model_timeout
    request.output_role = assistant_role
    if isinstance(model, ModelInfo):
        api_key = model.api_key
    else:
        raise HTTPException(
            status_code = 503,
            detail = "Error: Model API key not found",
        )
    request.key = api_key
    
    print_request_info(
        user_id = user_id,
        api = model,
        user_input = user_input,
        user_info = user_info,
        role_name = role_name,
    )

    # 设置请求对象的参数信息
    request.user_name = user_info.display_username()
    if configs.remove_reasoning_prompt is not None:
        request.remove_reasoning_prompt = configs.remove_reasoning_prompt
    else:
        request.remove_reasoning_prompt = global_configs.context.remove_reasoning_prompt
    
    if configs.temperature is not None:
        request.temperature = configs.temperature
    else:
        request.temperature = global_configs.model.default_temperature
    
    if configs.top_p is not None:
        request.top_p = configs.top_p
    else:
        request.top_p = global_configs.model.default_top_p
    
    if configs.frequency_penalty is not None:
        request.frequency_penalty = configs.frequency_penalty
    else:
        request.frequency_penalty = global_configs.model.default_frequency_penalty
    
    if configs.presence_penalty is not None:
        request.presence_penalty = configs.presence_penalty
    else:
        request.presence_penalty = global_configs.model.default_presence_penalty
    
    if configs.max_tokens is not None:
        request.max_tokens = configs.max_tokens
    else:
        request.max_tokens = global_configs.model.default_max_tokens
    
    if configs.max_completion_tokens is not None:
        request.max_completion_tokens = configs.max_completion_tokens
    else:
        request.max_completion_tokens = global_configs.model.default_max_completion_tokens
    
    if configs.stop is not None:
        request.stop = configs.stop
    else:
        request.stop = global_configs.model.default_stop
    
    if thinking is not None:
        request.thinking = thinking
    elif configs.thinking is not None:
        request.thinking = configs.thinking
    else:
        request.thinking = global_configs.model.default_thinking
    
    if configs.reasoning_effort is not None:
        request.reasoning_effort = configs.reasoning_effort
    else:
        request.reasoning_effort = global_configs.model.default_reasoning_effort
    
    if configs.send_user_id is not None:
        request.send_user_id = configs.send_user_id
    else:
        request.send_user_id = global_configs.callapi.send_user_id
    
    request.stream = global_configs.model.stream
    request.stream_options.include_obfuscation = global_configs.callapi.include_obfuscation
    request.stream_options.include_usage = global_configs.callapi.include_usage

    return request