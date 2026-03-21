import aiofiles

from ..._resource import Resource
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi import HTTPException, Query
from PathProcessors import validate_path
from pathlib import Path

from ....Global_Config_Manager import ConfigManager

@Resource.app.get("/static/{path:path}")
async def static_file(path: str, text_encoding: str | None = Query(None)):
    """Return static files"""
    static_dir = Path(ConfigManager.get_configs().static.static_dir)
    if not validate_path(
        base_path=static_dir,
        new_path=path
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    base_path = static_dir / path
    if not base_path.exists():
        raise HTTPException(status_code=404, detail="Not Found")
    
    if base_path.is_dir():
        raise HTTPException(status_code=403, detail="Target is a directory")

    if text_encoding is None:
        return FileResponse(static_dir / path)
    else:
        async with aiofiles.open(static_dir / path, mode="r", encoding=text_encoding) as f:
            text = await f.read()
        return PlainTextResponse(
            text,
            status_code = 200,
        )