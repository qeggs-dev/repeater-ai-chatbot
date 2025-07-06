from .._resource import (
    app,
    chat
)
from fastapi import (
    HTTPException
)
from fastapi.responses import (
    StreamingResponse
)
from io import BytesIO
import zipfile
import json


@app.get("/userdata/file/{user_id}.zip")
async def get_userdata_file(user_id: str):
    """
    Endpoint for getting userdata file
    """
    # 创建虚拟文件缓冲区
    buffer = BytesIO()

    # 创建zip文件并写入
    with zipfile.ZipFile(buffer, "w") as zipf:
        zipf.writestr("user_context.json", json.dumps(await chat.context_manager.load(user_id = user_id, default = {}), indent = 4, ensure_ascii=False))
        zipf.writestr("user_config.json", json.dumps(await chat.user_config_manager.load(user_id = user_id, default = []), indent = 4, ensure_ascii=False))
        zipf.writestr("user_prompt.json", json.dumps(await chat.prompt_manager.load(user_id = user_id, default = ""), indent = 4, ensure_ascii=False))
    buffer.seek(0)

    # 返回zip文件
    return StreamingResponse(buffer, media_type = "application/zip")