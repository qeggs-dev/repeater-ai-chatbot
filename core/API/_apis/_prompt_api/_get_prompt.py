from ...._resource import (
    chat,
    app
)
from fastapi.responses import (
    PlainTextResponse
)
from loguru import logger

@app.get("/userdata/prompt/get/{user_id}")
async def get_prompt(user_id: str):
    """
    Endpoint for setting prompt

    Args:
        user_id (str): User ID
    
    Returns:
        PlainTextResponse: User's prompt
    """
    # 获取用户ID为user_id的提示词
    prompt = await chat.prompt_manager.load(user_id)

    logger.info("Get prompt", user_id=user_id)

    # 返回提示词内容
    return PlainTextResponse(prompt)