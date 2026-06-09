from fastapi.responses import (
    ORJSONResponse
)
from .....special_exception import HTTPException
from .....repeater_main import RepeaterMain
from ._router import chat_router

@chat_router.get("/buffer/{user_id}")
async def get_chat_buffer_api(user_id: str):
    server = RepeaterMain.get_now_server()  
    if user_id not in server.runtime.content_buffers_pools:
        raise HTTPException(
            status_code = 404,
            detail = "This user does not have a task currently being generated."
        )
    task_context_buffers = await server.runtime.content_buffers_pools.get(user_id)
    buffers = {
        task_id: {
            "reasoning": str(buffer.reasoning_buffer),
            "content": str(buffer.content_buffer),
        } for task_id, buffer in task_context_buffers.items()
    }

    return ORJSONResponse(
        content = {
            "user_id": user_id,
            "buffers": buffers
        }
    )
    