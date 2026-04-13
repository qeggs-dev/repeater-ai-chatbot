from fastapi.responses import (
    ORJSONResponse
)
from ..._resource import Resource

@Resource.app.post("/chat/break/{user_id}")
async def chat_break_api(user_id: str):
    cancel_count = await Resource.chat_task_pool.cancel_tasks(user_id)
    return ORJSONResponse(
        {
            "code": 200,
            "msg": f"Cancel {cancel_count} tasks.",
            "cancel_count": cancel_count
        }
    )