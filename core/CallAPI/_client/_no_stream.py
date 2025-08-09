# ==== 标准库 ==== #
from typing import (
    Any,
    Awaitable,
    AsyncIterator,
    Callable,
)

# ==== 第三方库 ==== #
import openai

# ==== 自定义库 ==== #
from .._object import (
    Request,
    Response,
)
from .._parser import (
    CallAPI,
    StreamAPI
)
from .._exceptions import *
from ._client import ClientBase

class ClientNoStream(ClientBase):
    """Client without stream"""
    
    async def submit_Request(self, user_id:str, request: Request) -> Response:
        """提交请求，并等待API返回结果"""
        try:
            response, client = await self.coroutine_pool.submit(self._submit_task(user_id, request), user_id = user_id)
        except openai.NotFoundError:
            raise ModelNotFoundError(request.model)
        except openai.APIConnectionError:
            raise APIConnectionError(f"{request.url} Connection Failed")
        
        if isinstance(response, Response):
            processed_response = await self._preprocess_response(
                user_id=user_id,
                request=request,
                response=response
            )
            return processed_response
        else:
            async def stream_generator():
                try:
                    async for chunk in response:
                        pass
                finally:
                    processed_response = await self._preprocess_response(
                        user_id=user_id,
                        request=request,
                        response=client.last_response
                    )
                return processed_response
            return stream_generator()
    
    async def _submit_task(self, user_id: str, request: Request):
        if request.stream:
            client = StreamAPI()
        else:
            client = CallAPI()
        return await client.call(
            user_id = user_id,
            request = request
        ), client