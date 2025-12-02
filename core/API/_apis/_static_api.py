from .._resource import app
from fastapi.responses import FileResponse
from fastapi import HTTPException
from PathProcessors import validate_path
from pathlib import Path

from ...Global_Config_Manager import ConfigManager

@app.get('/favicon.ico')
async def favicon_ico():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.ico")

@app.get('/favicon.png')
async def favicon_png():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.png")

@app.get('/favicon.svg')
async def favicon_svg():
    """Return favicon"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "favicon.svg")

@app.get('/robots.txt')
async def robots():
    """Return robots.txt"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    return FileResponse(static_dir / "robots.txt")

@app.get('/static/{path:path}')
async def static(path: str):
    """Return static files"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    if not validate_path(
        base_path=static_dir,
        new_path=path
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    return FileResponse(static_dir / path)