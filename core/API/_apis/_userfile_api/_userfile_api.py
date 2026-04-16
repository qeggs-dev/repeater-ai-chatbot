import asyncio
from ..._server import Server
from ....Context_Manager import (
    ContextObject
)
from fastapi import (
    HTTPException
)
from fastapi.responses import (
    StreamingResponse
)
from loguru import logger
from io import BytesIO
from ._make_user_file import (
    make_user_file
)


@Server.app.get("/userdata/file/{user_id}.zip")
async def get_userdata_file(user_id: str):
    """
    Endpoint for getting userdata file

    Args:
        user_id (str): User ID

    Returns:
        StreamingResponse: File stream
    """
    # 创建虚拟文件缓冲区
    buffer = BytesIO()
    context_loader = await Server.core.get_context_loader()
    context = await context_loader.load_context(user_id = user_id)
    prompt = await Server.core.prompt_manager.load(user_id = user_id, default = "")
    config = await Server.core.user_config_manager.load(user_id = user_id)
    
    await asyncio.to_thread(
        make_user_file,
        file = buffer,
        context = context,
        prompt = prompt,
        user_configs = config
    )

    logger.info(f"Downloaded userdata file", user_id = user_id)

    # 返回zip文件
    return StreamingResponse(buffer, media_type = "application/zip")