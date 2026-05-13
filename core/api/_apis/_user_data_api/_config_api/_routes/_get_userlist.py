from ......repeater_main import RepeaterMain
from .._router import config_router
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@config_router.get("/userlist")
async def get_config_userlist():
    """
    Endpoint for getting config userlist

    Returns:
        ORJSONResponse: A JSON response containing the list of user IDs
    """
    server = RepeaterMain.get_now_server()

    # 获取所有用户ID
    userid_list = await server.runtime.user_config_manager.get_all_user_id()

    logger.info(f"Get user config userlist")

    # 返回用户ID列表
    return ORJSONResponse(userid_list)