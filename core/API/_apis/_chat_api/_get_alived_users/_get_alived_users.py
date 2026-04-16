from fastapi.responses import (
    ORJSONResponse
)
from ...._server import Server
from ._models import TasksIDResponse, UserInfo

@Server.app.get("/chat/alived_users")
async def get_alived_users_api():
    ids = Server.core.content_buffers_pool.ids
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
            buffer = await Server.core.content_buffers_pool.get(id)
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
