from ...._resource import (
    chat,
    app
)
from fastapi.responses import (
    PlainTextResponse
)
from loguru import logger

@app.delete("/userdata/context/delete/{user_id}")
async def delete_context(user_id: str):
    """
    Endpoint for deleting context

    Args:
        user_id (str): User ID

    Returns:
        PlainTextResponse: Success text for deleting context
    """
    # 删除用户ID为user_id的上下文
    await chat.context_manager.delete(user_id)

    logger.info("Delete Context", user_id = user_id)

    # 返回成功文本
    return PlainTextResponse("Context deleted successfully")