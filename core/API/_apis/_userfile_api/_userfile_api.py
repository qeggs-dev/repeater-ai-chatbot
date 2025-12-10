from ..._resource import (
    app,
    chat
)
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


@app.get("/userdata/file/{user_id}.zip")
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
    context_loader = await chat.get_context_loader()
    context = await context_loader.get_context_object(user_id = user_id)
    config = await chat.user_config_manager.load(user_id = user_id)
    prompt = await chat.prompt_manager.load(user_id = user_id, default = "")
    
    make_user_file(
        file = buffer,
        context = context,
        prompt = prompt,
        user_configs = config
    )

    logger.info(f"downloaded userdata file", user_id = user_id)

    # 返回zip文件
    return StreamingResponse(buffer, media_type = "application/zip")