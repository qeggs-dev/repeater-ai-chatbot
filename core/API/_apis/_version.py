from .._resource import Resource
from .._info import __version__ as __api_version__
from ..._info import __version__ as __core_version__
from fastapi.responses import (
    ORJSONResponse,
    PlainTextResponse
)

versions = {
    "core": __core_version__,
    "api": __api_version__
}

@Resource.app.route("/version")
def version():
    """
    Return the version of the API and the core
    """
    return ORJSONResponse(versions)

@Resource.app.route("/version/{module}")
def module_version(module: str):
    """
    Return the version of the specified module
    """
    if module in versions:
        return PlainTextResponse(versions[module])
    else:
        return PlainTextResponse(
            "Module not found",
            status_code = 404
        )
