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
    Delta
)
from .._parser import (
    CallAPI,
    StreamAPI
)
from .._exceptions import *
from ._client import ClientBase

class ClientStream(ClientBase):
    """Client with stream"""
    
    async def submit_Request(self, user_id:str, request: Request, get_response: Callable[[Response], Awaitable[None]] | None = None) -> AsyncIterator[Delta]:
        """提交请求，并等待API返回结果"""
        try:
            response, client = await self.coroutine_pool.submit(self._submit_task(user_id, request), user_id = user_id)
        except openai.NotFoundError:
            raise ModelNotFoundError(request.model)
        except openai.APIConnectionError:
            raise APIConnectionError(f"{request.url} Connection Failed")
        async def stream_generator():
            try:
                async for chunk in response:
                    yield chunk
            finally:
                processed_response = await self._preprocess_response(
                    user_id=user_id,
                    request=request,
                    response=response
                )
                if callable(get_response):
                    await get_response(processed_response)
        return stream_generator()
    
    
    async def _submit_task(self, user_id: str, request: Request):
        if request.stream:
            client = StreamAPI()
        else:
            raise StreamNotAvailable("When request.stream == True, the stream is not available.")
        return await client.call(
            user_id = user_id,
            request = request
        ), client
    