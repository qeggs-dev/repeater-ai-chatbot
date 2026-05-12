from ......server import RepeaterMain
from .._router import prompt_router
from fastapi.responses import (
    PlainTextResponse
)
from loguru import logger

@prompt_router.get("/get/{user_id}")
@prompt_router.get("/get/{user_id}.md")
async def get_prompt(user_id: str):
    """
    Endpoint for setting prompt

    Args:
        user_id (str): User ID
    
    Returns:
        PlainTextResponse: User's prompt
    """
    server = RepeaterMain.get_now_server()
    runtime = server.runtime

    # 获取用户ID为user_id的提示词
    prompt = await runtime.prompt_manager.load(user_id = user_id)

    logger.info("Get prompt", user_id=user_id)

    # 返回提示词内容
    return PlainTextResponse(prompt)