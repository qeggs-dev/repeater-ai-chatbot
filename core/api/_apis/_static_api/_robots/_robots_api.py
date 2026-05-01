from .._router import static_router
from fastapi.responses import FileResponse
from pathlib import Path

from .....global_config_manager import ConfigManager

@static_router.get("/robots.txt")
async def robots():
    """Return robots.txt"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "robots.txt")