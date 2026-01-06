from ...._resource import Resource
from fastapi.responses import FileResponse
from pathlib import Path

from .....Global_Config_Manager import ConfigManager

@Resource.app.get("/favicon.ico")
async def favicon_ico():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.ico")

@Resource.app.get("/favicon.png")
async def favicon_png():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.png")

@Resource.app.get("/favicon.svg")
async def favicon_svg():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.svg")