from fastapi.responses import (
    ORJSONResponse
)
from .....special_exception import HTTPException
from .....server import Server
from ._router import chat_router

@chat_router.get("/buffer/{user_id}")
async def get_chat_buffer_api(user_id: str):
    if user_id not in Server.core.runtime.content_buffers_pool:
        raise HTTPException(
            status_code = 404,
            detail = "This user does not have a task currently being generated."
        )
    buffers = await Server.core.runtime.content_buffers_pool.get(user_id)

    return ORJSONResponse(
        content = {
            "reasoning": str(buffers.reasoning_buffer),
            "content": str(buffers.content_buffer)
        }
    )
    