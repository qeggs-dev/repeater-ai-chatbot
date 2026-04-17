from fastapi.responses import (
    ORJSONResponse
)
from ....SpecialException import HTTPException
from ...._server import Server

@Server.app.get("/chat/buffer/{user_id}")
async def get_chat_buffer_api(user_id: str):
    if user_id not in Server.core.content_buffers_pool:
        raise HTTPException(
            status_code = 404,
            message = "This user does not have a task currently being generated."
        )
    buffers = await Server.core.content_buffers_pool.get(user_id)

    return ORJSONResponse(
        content = {
            "reasoning": str(buffers.reasoning_buffer),
            "content": str(buffers.content_buffer)
        }
    )
    