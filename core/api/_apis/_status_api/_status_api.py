from ....server import RepeaterMain
from ._router import status_router
from fastapi.responses import ORJSONResponse

@status_router.get("/core/task/{user_id}")
def get_core_task_status(user_id: str):
    server = RepeaterMain.get_now_server()
    runtime = server.runtime
    if runtime.task_status_map.contains(user_id):
        return ORJSONResponse(
            content = runtime.task_status_map.get_status(user_id)
        )
    else:
        return ORJSONResponse(
            content = []
        )