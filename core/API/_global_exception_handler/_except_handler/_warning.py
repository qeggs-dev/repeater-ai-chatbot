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

async def warning_handler(warning: Warning) -> None:
    warning_time = datetime.now()

    traceback_str = traceback.format_exc()
    if ConfigManager().get_configs().global_exception_handler.traceback_save_to:
        await save_error_traceback(warning_time, traceback_str)

    # 记录异常日志
    logger.exception(
        "Warning: {message}\n{traceback}",
        user_id = "[Global Exception Recorder]",
        message = str(warning),
        traceback = traceback_str
    )