# ==== 标准库 ==== #
import asyncio
from typing import (
    Any,
    Awaitable,
    AsyncIterator,
    Callable,
)

# ==== 第三方库 ==== #
from loguru import logger

# ==== 自定义库 ==== #
from .._objects import (
    Request,
    Response,
    Delta,
    Runtime
)
from .._caller import (
    StreamAPI
)
from .._exceptions import StreamNotAvailable
from .._caller import StreamingResponseGenerationLayer
from ._client import ClientBase

class StreamClient(ClientBase):
    """Client with stream"""
    
    async def submit_request(
            self,
            user_id:str,
            request: Request,
            runtime: Runtime,
            chunk_callback: Callable[[Delta], Awaitable[None]] | None = None
        ) -> Response:
        """提交请求，并等待API返回结果"""
        generator: AsyncIterator[Delta] = self._submit_task(user_id, request, runtime)
        wraping_generator = StreamingResponseGenerationLayer(
            user_id = user_id,
            request = request,
            content_buffer = runtime.content_buffer,
            response_iterator = generator
        )
        async for delta in wraping_generator:
            if chunk_callback is not None:
                await chunk_callback(delta)

        await self._preprocess_response(user_id, request, wraping_generator.response, runtime)
        
        return wraping_generator.response
    
    async def _submit_task(self, user_id: str, request: Request, runtime: Runtime) -> AsyncIterator[Delta]:
        if request.stream:
            client = StreamAPI()
        else:
            raise StreamNotAvailable("When request.stream == True, the stream is not available.")
        generator = await client.call(
            user_id = user_id,
            request = request,
            runtime = runtime
        )

        async for delta in generator:
            yield delta