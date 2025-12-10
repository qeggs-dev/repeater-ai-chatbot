from ...._resource import app
from fastapi.responses import FileResponse
from pathlib import Path

from .....Global_Config_Manager import ConfigManager

@app.get("/robots.txt")
async def robots():
    """Return robots.txt"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "robots.txt")