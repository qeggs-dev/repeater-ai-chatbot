from .._resource import app, configs
from fastapi.responses import FileResponse

@app.get('/favicon.ico')
async def favicon_ico():
    """Return favicon"""
    static_dir = configs.get_config('static.base_path').get_value(str)
    return FileResponse(f'{static_dir}/favicon.ico')

@app.get('/favicon.png')
async def favicon_png():
    """Return favicon"""
    static_dir = configs.get_config('static.base_path').get_value(str)
    return FileResponse(f'{static_dir}/favicon.png')

@app.get('/favicon.svg')
async def favicon_svg():
    """Return favicon"""
    static_dir = configs.get_config('static.base_path').get_value(str)
    return FileResponse(f'{static_dir}/favicon.svg')

@app.get('/robots.txt')
async def robots():
    """Return robots.txt"""
    static_dir = configs.get_config('static.base_path').get_value(str)
    return FileResponse(f'{static_dir}/robots.txt')

@app.get('/static/{path:path}')
async def static(path: str):
    """Return static files"""
    static_dir = configs.get_config('static.base_path').get_value(str)
    return FileResponse(f'{static_dir}/{path}')