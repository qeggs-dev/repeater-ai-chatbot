# ==== 标准库 ==== #
from datetime import datetime

# ==== 第三方库 ==== #
import openai
from openai.types.chat import ChatCompletion
from openai.types.completion import Completion
from openai import NOT_GIVEN
from loguru import logger

# ==== 自定义库 ==== #
from .._objects import (
    Request,
    Runtime,
    Response,
)
from ....request_log import TimeStamp
from ._call_api_base import CallNstreamAPIBase
from .._exceptions import *
from ._translation_openai_response import translation_openai_response

class CallAPI(CallNstreamAPIBase):
    async def _openai_call(self, user_id:str, request: Request, runtime: Runtime) -> Response:
        """调用API"""
        # 检查参数
        assert isinstance(user_id, str), "user_id must be str"
        assert isinstance(request, Request), "request must be Request"
        assert isinstance(runtime, Runtime), "runtime must be Runtime"

        if request.stream:
            raise NotImplementedError("Stream API not implemented")

        with runtime.status_stack.enter("Init objects"):
            # 创建模型响应对象
            model_response = runtime.response

        with runtime.status_stack.enter("Create OpenAI Client"):
            # 创建OpenAI Client
            logger.info(f"Created OpenAI Client", user_id = user_id)
            client = self.get_client(
                request = request,
                runtime = runtime
            )
        
        with runtime.status_stack.enter("Write calling log base data"):
            # 写入调用日志基础数据
            model_response.request_log.url = request.url
            model_response.request_log.user_id = user_id
            model_response.request_log.user_name = request.user_name
            model_response.request_log.model = request.model
            model_response.request_log.stream = request.stream

        # 如果上下文为空，则抛出异常
        with runtime.status_stack.enter("Check context"):
            if not request.context:
                raise ValueError("context is required")
        
        with runtime.status_stack.enter("Make extra body"):
            extra_body = {}

            if request.thinking is not None:
                with runtime.status_stack.enter("thinking"):
                    if request.thinking:
                        extra_body["thinking"] = {
                            "type": "enabled"
                        }
                    else:
                        extra_body["thinking"] = {
                            "type": "disabled"
                        }
            
            if request.reasoning_effort is not None:
                with runtime.status_stack.enter("reasoning_effort"):
                    extra_body["reasoning_effort"] = request.reasoning_effort.value
            
            if request.send_user_id:
                with runtime.status_stack.enter("user_id"):
                    extra_body["user_id"] = user_id

        # 发送请求
        with runtime.status_stack.enter("Send Request"):
            logger.info(f"Send Request", user_id = user_id)
            request_start_time = TimeStamp()
            response = await self._send_request(
                user_id = user_id,
                request = request,
                runtime = runtime,
                client = client,
                extra_body = extra_body,
                stream = False,
            )
            request_end_time = TimeStamp()

        with runtime.status_stack.enter("Processing Response"):
            model_response.request_log.request_start_time = request_start_time
            model_response.request_log.request_end_time = request_end_time
            return translation_openai_response(
                request = request,
                response = response,
                runtime = runtime,
                print_file = self._print_file
            )