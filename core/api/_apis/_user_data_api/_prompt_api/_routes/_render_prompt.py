from ......server import RepeaterMain
from ......global_config_manager import ConfigManager
from .._router import prompt_router
from fastapi.responses import (
    PlainTextResponse
)
from loguru import logger

@prompt_router.get("/render/{user_id}")
@prompt_router.get("/render/{user_id}.md")
async def render_prompt(user_id: str):
    """
    Render prompt

    Args:
        user_id (str): User ID
    
    Returns:
        PlainTextResponse: Rendered prompt
    """
    server = RepeaterMain.get_now_server()
    runtime = server.core.runtime
    context_loader = server.core.get_context_loader()
    prompt = await context_loader.load_prompt(
        user_id = user_id,
        static_resources_client = runtime.static_resources_client,
        template_parser = await server.core.get_template_parser(
            user_config = await runtime.user_config_manager.load(user_id),
            global_config = ConfigManager.get_configs(),
        )
    )

    logger.info("Get prompt", user_id=user_id)

    # 返回提示词内容
    return PlainTextResponse(prompt.content)