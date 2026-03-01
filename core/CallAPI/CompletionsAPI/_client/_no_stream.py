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
    Delta
)
from .._caller import (
    CallAPI,
    StreamAPI
)
from ....Status_Map import StatusMap
from .._exceptions import *
from .._caller import StreamingResponseGenerationLayer
from ._client import ClientBase

class ClientNoStream(ClientBase):
    """Client without stream"""
    
    async def submit_request(self, user_id:str, request: Request, status_map: StatusMap[str, str]) -> Response:
        """提交请求，并等待API返回结果"""
        try:
            response = await self._submit_task(user_id, request, status_map)
            if not isinstance(response, Response):
                generator = StreamingResponseGenerationLayer(user_id, request, response)
                async for chunk in generator:
                    pass
                output = generator.response
            else:
                output = response

            await self._preprocess_response(user_id, request, output, status_map)

        except openai.NotFoundError:
            raise ModelNotFoundError(request.model)
        except openai.APIConnectionError:
            raise APIConnectionError(f"{request.url} Connection Failed")
        
        return output
    
    async def _submit_task(self, user_id: str, request: Request, status_map: StatusMap[str, str]) -> AsyncIterator[Delta] | Response:
        try:
            if request.stream:
                client = StreamAPI()
                call = client.call(
                    user_id = user_id,
                    request = request,
                    status_map = status_map
                )
            else:
                client = CallAPI()
                call = await client.call(
                    user_id = user_id,
                    request = request,
                    status_map = status_map
                )
            return call
        except openai.BadRequestError as e:
            if e.code in range(400, 500):
                logger.error(f"BadRequestError: {e}", user_id = user_id)
                raise BadRequestError(e.message)
            elif e.code in range(500, 600):
                logger.error(f"API Server Error: {e}", user_id = user_id)
                raise APIServerError(e.message)
        except Exception as e:
            logger.error(f"Error: {e}", user_id = user_id)
            raise CallApiException(e) from e