import orjson
import asyncio

from typing import AsyncIterator
from environs import Env
env = Env()
env.read_env()
from fastapi.responses import (
    ORJSONResponse,
    StreamingResponse
)
from fastapi.exceptions import (
    HTTPException
)
from ..._resource import Resource

@Resource.app.post("/chat/break/{user_id}")
async def chat_break_api(user_id: str):
    await Resource.chat_task_pool.cancel_tasks(user_id)
    return ORJSONResponse(
        {
            "code": 200,
            "msg": "success"
        }
    )