from ..._resource import Resource
from ....Global_Config_Manager import ConfigManager
from fastapi.responses import FileResponse, HTMLResponse, ORJSONResponse
from pathlib import Path
from ._default_web import DEFAULT_WEB_HTML
from PathProcessors import validate_path

@Resource.app.get("/")
@Resource.app.get("/index.html")
async def index_web():
    if ConfigManager.get_configs().web.index_web_file:
        index_web_file = Path(ConfigManager.get_configs().web.index_web_file)
        if index_web_file.exists() and index_web_file.is_file():
            return FileResponse(index_web_file)
        
    # 该默认网页由AI生成
    return HTMLResponse("\n".join(DEFAULT_WEB_HTML))

@Resource.app.get("/web/{file_name}")
async def web_file(file_name: str):
    web_directory = Path(ConfigManager.get_configs().web.web_directory)
    if not validate_path(web_directory, file_name):
        return ORJSONResponse(
            {
                "error": "Invalid path"
            },
            status_code=400
        )
    
    web_file_path = web_directory / file_name
    if web_file_path.exists() and web_file_path.is_file():
        return FileResponse(web_file_path)
    else:
        return ORJSONResponse(
            {
                "error": "File not found"
            },
            status_code=404
        )