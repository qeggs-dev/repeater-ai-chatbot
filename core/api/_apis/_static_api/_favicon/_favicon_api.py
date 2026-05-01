from .._router import static_router
from fastapi.responses import FileResponse
from pathlib import Path

from .....global_config_manager import ConfigManager

@static_router.get("/favicon.ico")
async def favicon_ico():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.ico")

@static_router.get("/favicon.png")
async def favicon_png():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.png")

@static_router.get("/favicon.svg")
async def favicon_svg():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.svg")