from ....server import Server
from ._router import status_router
from fastapi.responses import ORJSONResponse

@status_router.get("/core/task/{user_id}")
def get_core_task_status(user_id: str):
    if Server.core.runtime.task_status_map.contains(user_id):
        return ORJSONResponse(
            content = Server.core.runtime.task_status_map.get_status(user_id)
        )
    else:
        return ORJSONResponse(
            content = []
        )