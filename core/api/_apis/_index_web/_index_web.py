from ....server import Server
from ....global_config_manager import ConfigManager
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
from ._default_web import DEFAULT_WEB_HTML

@Server.app.get("/")
@Server.app.get("/index.html")
async def index_web():
    if ConfigManager.get_configs().web.index_web_file:
        index_web_file = Path(ConfigManager.get_configs().web.index_web_file)
        if index_web_file.exists() and index_web_file.is_file():
            return FileResponse(index_web_file)
    
    return HTMLResponse("\n".join(DEFAULT_WEB_HTML))