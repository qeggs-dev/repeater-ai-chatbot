from fastapi.responses import (
    ORJSONResponse
)
from ......repeater_main import RepeaterMain
from ._models import TasksIDResponse, UserInfo
from .._router import chat_router

@chat_router.get("/alived_users")
async def get_alived_users_api():
    server = RepeaterMain.get_now_server()
    ids = server.runtime.content_buffers_pool.ids
    if len(ids) == 0:
        return ORJSONResponse(
            content=TasksIDResponse(
                message="No users online",
                count=0
            ).model_dump()
        )
    else:
        users: dict[str, UserInfo] = {}
        for id in ids:
            buffer = await server.runtime.content_buffers_pool.get(id)
            users[id] = UserInfo(
                generated_length=len(buffer)
            )
        return ORJSONResponse(
            content=TasksIDResponse(
                message = f"There are currently {len(users)} users in the build process.",
                count = len(users),
                users = users
            ).model_dump()
        )
