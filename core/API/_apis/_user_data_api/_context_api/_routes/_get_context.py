from ....._resource import Resource
from fastapi.responses import (
    ORJSONResponse,
)
from loguru import logger

@Resource.app.get("/userdata/context/get/{user_id}")
async def get_context(user_id: str):
    """
    Endpoint for getting context

    Args:
        user_id (str): User ID
    
    Returns:
        ORJSONResponse: User context
    """
    # 从chat.context_manager中加载用户ID为user_id的上下文
    context_loader = await Resource.core.get_context_loader()
    context = await context_loader.load_context(user_id)

    logger.info(f"Get Context", user_id = user_id)

    # 返回JSON格式的上下文
    return ORJSONResponse(context.context)