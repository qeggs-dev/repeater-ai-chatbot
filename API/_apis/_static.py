from .._resource import app
from fastapi.responses import FileResponse

@app.get('/favicon.ico')
async def favicon():
    """Return favicon"""
    return FileResponse('static/favicon.ico')