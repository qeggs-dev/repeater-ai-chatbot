from ...._resource import (
    chat,
    app
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@app.get("/userdata/config/userlist")
async def get_config_userlist():
    """
    Endpoint for getting config userlist

    Returns:
        ORJSONResponse: A JSON response containing the list of user IDs
    """

    # 获取所有用户ID
    userid_list = await chat.user_config_manager.get_all_user_id()

    logger.info(f"Get user config userlist")

    # 返回用户ID列表
    return ORJSONResponse(userid_list)