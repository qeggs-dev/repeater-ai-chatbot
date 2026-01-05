import time
import asyncio
import traceback
from loguru import logger
from datetime import datetime
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError

from ....CriticalException import CriticalException
from ....Global_Config_Manager import ConfigManager
from .._shutdown_server import shutdown_server
from .._save_error_traceback import save_error_traceback
from .._error_output_model import ErrorResponse

async def base_exception_handler(exception: Warning) -> None:
    # 记录异常日志
    logger.warning(
        "Catch Other Exception: \n{message}",
        user_id = "[Global Exception Recorder]",
        message = str(exception)
    )