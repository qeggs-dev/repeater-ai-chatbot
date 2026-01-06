from ..._resource import Resource
from ....Global_Config_Manager import ConfigManager
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
from ._default_web import DEFAULT_WEB_HTML

@Resource.app.get("/")
@Resource.app.get("/index.html")
async def index_web():
    if ConfigManager.get_configs().web.index_web_file:
        index_web_file = Path(ConfigManager.get_configs().web.index_web_file)
        if index_web_file.exists() and index_web_file.is_file():
            return FileResponse(index_web_file)
        
    # 该默认网页由AI生成
    return HTMLResponse("\n".join(DEFAULT_WEB_HTML))