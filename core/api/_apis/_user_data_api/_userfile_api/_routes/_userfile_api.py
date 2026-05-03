import asyncio
from ......server import Server
from .._router import user_file_router
from fastapi.responses import (
    StreamingResponse
)
from loguru import logger
from io import BytesIO
from .._auxiliary import (
    make_user_file
)


@user_file_router.get("/file/{user_id}.zip")
async def get_userdata_file(user_id: str):
    """
    Endpoint for getting userdata file

    Args:
        user_id (str): User ID

    Returns:
        Response: File Response
    """
    # 创建虚拟文件缓冲区
    buffer = BytesIO()
    context_loader = Server.core.get_context_loader()
    context = await context_loader.load_context(user_id = user_id)
    prompt = await Server.core.runtime.prompt_manager.load(user_id = user_id, default = "")
    config = await Server.core.runtime.user_config_manager.load(user_id = user_id)
    
    await asyncio.to_thread(
        make_user_file,
        file = buffer,
        context = context,
        prompt = prompt,
        user_configs = config
    )

    logger.info(f"Downloaded userdata file", user_id = user_id)

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