from ...._resource import Resource
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@Resource.app.get("/userdata/context/length/{user_id}")
async def get_context_length(user_id: str):
    """
    Endpoint for getting context

    Args:
        user_id (str): The user ID
    
    Returns:
        ORJSONResponse: The JSON response containing the context length
    """
    # 从chat.context_manager中加载用户ID为user_id的上下文
    context_loader = await Resource.core.get_context_loader()
    context = await context_loader.load_context(user_id)
    
    logger.info(f"Get Context length", user_id = user_id)

    # 返回ORJSONResponse，包含上下文的总长度和上下文的长度
    return ORJSONResponse(
        {
            "total_context_length": context.total_length,
            "context_length": context.context_item_length,
            "average_content_length": context.average_length
        }
    )