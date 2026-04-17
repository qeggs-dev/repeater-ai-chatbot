from ....._server import Server
from fastapi.responses import FileResponse
from pathlib import Path

from .....Global_Config_Manager import ConfigManager

@Server.app.get("/robots.txt")
async def robots():
    """Return robots.txt"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "robots.txt")