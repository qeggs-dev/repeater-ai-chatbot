from ....._server import Server
from fastapi.responses import FileResponse
from pathlib import Path

from .....Global_Config_Manager import ConfigManager

@Server.app.get("/favicon.ico")
async def favicon_ico():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.ico")

@Server.app.get("/favicon.png")
async def favicon_png():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.png")

@Server.app.get("/favicon.svg")
async def favicon_svg():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.svg")