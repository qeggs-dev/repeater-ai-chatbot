from uvicorn import Server
from fastapi import Request, FastAPI
from fastapi.responses import Response
from typing import Callable, Awaitable

from ..global_config_manager import ConfigManager
from ..repeater_traceback import log_traceback

def middleware_factory(app: FastAPI, server: Server):
    @app.middleware("http")
    async def http_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        try:
            return await call_next(request)
        except Exception as e:
            return await log_traceback(e, server)
        except BaseException as e:
            if ConfigManager().get_configs().global_exception_handler.record_all_exceptions:
                await log_traceback(e, server)
            raise
    return http_middleware