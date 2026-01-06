from fastapi.responses import Response
from fastapi import Request
from typing import Callable, Awaitable

from .._resource import app
from ...Global_Config_Manager import ConfigManager
from ._except_handler import (
    exception_handler,
    warning_handler,
    base_exception_handler
)

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    try:
        return await call_next(request)
    except Exception as e:
        return await exception_handler(e)
    except BaseException as e:
        if ConfigManager().get_configs().global_exception_handler.record_all_exceptions:
            await base_exception_handler(e)
        raise