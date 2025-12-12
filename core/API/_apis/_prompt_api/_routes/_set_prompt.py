from ...._resource import (
    chat,
    app
)
from fastapi import Form
from fastapi.responses import (
    ORJSONResponse,
    PlainTextResponse
)
from loguru import logger

@app.put("/userdata/prompt/set/{user_id}")
async def set_prompt(user_id: str, prompt: str = Form(...)):
    """
    Endpoint for setting prompt

    Args:
        user_id (str): User ID
        prompt (str): Prompt content

    Returns:
        PlainTextResponse: Success message
    """
    # 设置用户ID为user_id的提示词为prompt
    await chat.prompt_manager.save(user_id, prompt)

    logger.info("Set prompt", user_id=user_id)

    # 返回成功文本
    return PlainTextResponse("Prompt set successfully")