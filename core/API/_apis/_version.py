from .._resource import app, __version__
from ..._core import __version__ as __core_version__
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse
)

@app.route('/version')
def version():
    """
    Return the version of the API and the core
    """
    return JSONResponse(
        {
        'core': __core_version__,
        'api': __version__
        }
    )

@app.route('/version/core')
def core_version():
    """
    Return the version of the core
    """
    return PlainTextResponse(
        __core_version__
    )

@app.route('/version/api')
def api_version():
    """
    Return the version of the API
    """
    return PlainTextResponse(
        __version__
    )
