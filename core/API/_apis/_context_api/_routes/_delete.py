from ...._resource import Resource
from fastapi.responses import (
    PlainTextResponse
)
from loguru import logger

@Resource.app.delete("/userdata/context/delete/{user_id}")
async def delete_context(user_id: str):
    """
    Endpoint for deleting context

    Args:
        user_id (str): User ID

    Returns:
        PlainTextResponse: Success text for deleting context
    """
    # 删除用户ID为user_id的上下文
    await Resource.core.context_manager.delete(user_id)

    logger.info("Delete Context", user_id = user_id)

    # 返回成功文本
    return PlainTextResponse("Context deleted")