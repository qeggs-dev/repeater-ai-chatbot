from ..._resource import app
from fastapi.responses import FileResponse
from fastapi import HTTPException
from PathProcessors import validate_path
from pathlib import Path

from ....Global_Config_Manager import ConfigManager

@app.get("/static/{path:path}")
async def static_file(path: str):
    """Return static files"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    if not validate_path(
        base_path=static_dir,
        new_path=path
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    return FileResponse(static_dir / path)