from ...._resource import Resource
from fastapi.responses import FileResponse
from pathlib import Path

from .....Global_Config_Manager import ConfigManager

@Resource.app.get("/robots.txt")
async def robots():
    """Return robots.txt"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "robots.txt")