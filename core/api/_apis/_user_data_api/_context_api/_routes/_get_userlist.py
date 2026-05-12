from ......server import RepeaterMain
from .._router import context_router
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@context_router.get("/userlist")
async def get_context_userlist():
    """
    Endpoint for getting context

    Returns:
        ORJSONResponse: A ORJSONResponse containing a list of user IDs
    """
    server = RepeaterMain.get_now_server()
    runtime = server.runtime

    # 从chat.context_manager中获取所有用户ID
    userid_list = await runtime.context_manager.get_all_user_id()

    logger.info(f"Get Context userlist")

    # 返回ORJSONResponse，包含所有用户ID
    return ORJSONResponse(userid_list)