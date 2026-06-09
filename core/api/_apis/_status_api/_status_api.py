from ....repeater_main import RepeaterMain
from ._router import status_router
from fastapi.responses import ORJSONResponse

@status_router.get("/core/task/{user_id}")
async def get_core_task_status(user_id: str):
    server = RepeaterMain.get_now_server()
    runtime = server.runtime
    if user_id in runtime.task_status_stacks:
        tasks = {}
        user_task_status_stack = await runtime.task_status_stacks.get(user_id)
        for task_id, task in user_task_status_stack.items():
            tasks[task_id] = task.get_status()
        return ORJSONResponse(
            content = {
                "contains": True,
                "tasks": tasks
            }
        )
    else:
        return ORJSONResponse(
            content = {
                "contains": False,
                "tasks": {}
            }
        )