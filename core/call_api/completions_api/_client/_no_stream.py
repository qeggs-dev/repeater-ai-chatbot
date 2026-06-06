# ==== 标准库 ==== #
from typing import (
    Any,
    Awaitable,
    AsyncIterator,
    Callable
)

# ==== 第三方库 ==== #
import openai
from loguru import logger

# ==== 自定义库 ==== #
from .._objects import (
    Request,
    Response,
    Delta,
    Runtime
)
from .._caller import (
    CallAPI,
    StreamAPI
)
from .._exceptions import *
from .._caller import StreamingResponseGenerationLayer
from ._client import ClientBase

class NoStreamClient(ClientBase):
    """Client without stream"""
    
    async def submit_request(
            self,
            user_id:str,
            request: Request,
            runtime: Runtime,
        ) -> Response:
        """提交请求，并等待API返回结果"""
        try:
            response = await self._submit_task(user_id, request, runtime)
            if not isinstance(response, Response):
                generator = StreamingResponseGenerationLayer(
                    user_id = user_id,
                    request = request,
                    runtime = runtime,
                    response_iterator = response
                )
                async for chunk in generator:
                    pass
                output = generator.response
            else:
                output = response

            await self._preprocess_response(user_id, request, output, runtime)

        except openai.NotFoundError:
            raise ModelNotFoundError(request.model)
        except openai.APIConnectionError:
            raise APIConnectionError(f"{request.url} Connection Failed")
        
        return output
    
    async def _submit_task(self, user_id: str, request: Request, runtime: Runtime) -> AsyncIterator[Delta] | Response:
        if request.stream:
            client = StreamAPI()
            call = await client.call(
                user_id = user_id,
                request = request,
                runtime = runtime
            )
        else:
            client = CallAPI()
            call = await client.call(
                user_id = user_id,
                request = request,
                runtime = runtime
            )
        return call