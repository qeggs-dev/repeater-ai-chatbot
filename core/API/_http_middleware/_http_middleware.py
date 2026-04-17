from fastapi.responses import Response
from fastapi import Request
from typing import Callable, Awaitable

from ..._server import Server
from ...Global_Config_Manager import ConfigManager
from ...Repeater_Traceback import WarningHandler, log_traceback

# 初始化警告处理器
warning_handler = WarningHandler()
warning_handler.inject()

@Server.app.middleware("http")
async def http_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    try:
        return await call_next(request)
    except Exception as e:
        return await log_traceback(e)
    except BaseException as e:
        if ConfigManager().get_configs().global_exception_handler.record_all_exceptions:
            await log_traceback(e)
        raise