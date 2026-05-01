from ......server import Server
from .._router import prompt_router
from fastapi.responses import (
    ORJSONResponse,
)
from loguru import logger

@prompt_router.get("/userlist")
async def get_prompt_userlist():
    """
    Endpoint for getting prompt user list

    Returns:
        ORJSONResponse: User ID list
    """
    # 获取所有用户ID
    userid_list = await Server.core.runtime.prompt_manager.get_all_user_id()

    logger.info("Get prompt user list")

    # 返回用户ID列表
    return ORJSONResponse(userid_list)
