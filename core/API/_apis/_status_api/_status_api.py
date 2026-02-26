from ..._resource import Resource
from fastapi.responses import ORJSONResponse

@Resource.app.get("/status/core/task/{user_id}")
def get_core_task_status(user_id: str):
    return ORJSONResponse(
        content = Resource.core.task_status_map.get_status(user_id)
    )