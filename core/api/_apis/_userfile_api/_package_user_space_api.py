import asyncio
from ....server import Server
from fastapi.responses import (
    StreamingResponse
)
from loguru import logger
from io import BytesIO
from ._package_user_space import package_user_space


@Server.app.get("/userdata/package_space/{user_id}.zip")
async def get_userdata_file(user_id: str):
    """
    Endpoint for package user space to zip file

    Args:
        user_id (str): User ID

    Returns:
        Response: File stream
    """
    # 创建虚拟文件缓冲区
    buffer = BytesIO()
    context_loader = await Server.core.get_context_loader()
    prompt_manager = Server.core.runtime.prompt_manager
    config_manager = Server.core.runtime.user_config_manager
    
    await package_user_space(
        user_id = user_id,
        context_loader = context_loader,
        prompt_manager = prompt_manager,
        config_manager = config_manager,
        file = buffer
    )

    logger.info(f"User {user_id} package space", user_id = user_id)

    # 获取文件大小
    buffer.seek(0, 2)
    file_size = buffer.tell()
    buffer.seek(0)

    # 返回zip文件
    return StreamingResponse(
        buffer,
        media_type = "application/octet-stream",
        headers = {
            "Content-Length": str(file_size),
        }
    )