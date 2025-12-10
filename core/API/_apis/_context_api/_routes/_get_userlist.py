from ...._resource import (
    chat,
    app
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@app.get("/userdata/context/userlist")
async def get_context_userlist():
    """
    Endpoint for getting context

    Returns:
        ORJSONResponse: A ORJSONResponse containing a list of user IDs
    """
    # 从chat.context_manager中获取所有用户ID
    userid_list = await chat.context_manager.get_all_user_id()

    logger.info(f"Get Context userlist")

    # 返回ORJSONResponse，包含所有用户ID
    return ORJSONResponse(userid_list)