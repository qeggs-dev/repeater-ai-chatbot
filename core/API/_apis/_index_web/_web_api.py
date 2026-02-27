from ..._resource import Resource
from ....Global_Config_Manager import ConfigManager
from fastapi.responses import FileResponse, ORJSONResponse
from pathlib import Path
from PathProcessors import validate_path

@Resource.app.get("/web/{file_name:path}")
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