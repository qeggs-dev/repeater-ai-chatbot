from .....Server import Server
from fastapi.responses import (
    ORJSONResponse,
)
from loguru import logger

@Server.app.get("/userdata/prompt/userlist")
async def get_prompt_userlist():
    """
    Endpoint for getting prompt user list

    Returns:
        ORJSONResponse: User ID list
    """
    # 获取所有用户ID
    userid_list = await Server.core.prompt_manager.get_all_user_id()

    logger.info("Get prompt user list")

    # 返回用户ID列表
    return ORJSONResponse(userid_list)
