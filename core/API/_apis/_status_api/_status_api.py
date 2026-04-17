from ....Server import Server
from fastapi.responses import ORJSONResponse

@Server.app.get("/status/core/task/{user_id}")
def get_core_task_status(user_id: str):
    if Server.core.task_status_map.contains(user_id):
        return ORJSONResponse(
            content = Server.core.task_status_map.get_status(user_id)
        )
    else:
        return ORJSONResponse(
            content = []
        )