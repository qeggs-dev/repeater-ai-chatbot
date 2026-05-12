from fastapi.responses import (
    ORJSONResponse
)
from ._router import chat_router
from .....server import RepeaterMain

@chat_router.post("/break/{user_id}")
async def chat_break_api(user_id: str):
    server = RepeaterMain.get_now_server()
    cancel_count = await server.core.runtime.chat_task_pool.cancel_tasks(user_id)
    return ORJSONResponse(
        {
            "code": 200,
            "msg": f"Cancel {cancel_count} tasks.",
            "cancel_count": cancel_count
        }
    )