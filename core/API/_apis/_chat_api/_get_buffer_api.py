from fastapi.responses import (
    ORJSONResponse
)
from ....SpecialException import HTTPException
from ..._resource import Resource

@Resource.app.get("/chat/buffer/{user_id}")
async def get_chat_buffer_api(user_id: str):
    if user_id not in Resource.core.content_buffers_pool:
        raise HTTPException(
            status_code = 404,
            message = "This user does not have a task currently being generated."
        )
    buffers = await Resource.core.content_buffers_pool.get(user_id)

    return ORJSONResponse(
        content = {
            "reasoning": str(buffers.reasoning_buffer),
            "content": str(buffers.content_buffer)
        }
    )
    