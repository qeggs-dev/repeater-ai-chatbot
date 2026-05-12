from ......server import RepeaterMain
from .._router import prompt_router
from fastapi import Form
from fastapi.responses import (
    ORJSONResponse,
    PlainTextResponse
)
from loguru import logger

@prompt_router.put("/set/{user_id}")
async def set_prompt(user_id: str, prompt: str = Form(...)):
    """
    Endpoint for setting prompt

    Args:
        user_id (str): User ID
        prompt (str): Prompt content

    Returns:
        PlainTextResponse: Success message
    """
    server = RepeaterMain.get_now_server()
    runtime = server.runtime

    # 设置用户ID为user_id的提示词为prompt
    await runtime.prompt_manager.save(
        user_id = user_id,
        data = prompt
    )

    logger.info("Set prompt", user_id=user_id)

    # 返回成功文本
    return PlainTextResponse("Prompt seted")