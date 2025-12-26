from ...._resource import (
    chat,
    app
)
from fastapi.responses import (
    PlainTextResponse
)
from loguru import logger

@app.delete("/userdata/prompt/delete/{user_id}")
async def delete_prompt(user_id: str):
    """
    Endpoint for deleting prompt

    Args:
        user_id (str): User ID

    Returns:
        PlainTextResponse: Success text for successful deletion
    """
    # 删除用户ID为user_id的提示词
    await chat.prompt_manager.delete(user_id)

    logger.info("Delete prompt", user_id=user_id)

    # 返回成功文本
    return PlainTextResponse("Prompt deleted")