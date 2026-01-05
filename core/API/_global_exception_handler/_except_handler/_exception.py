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


async def exception_handler(error: Exception) -> None:
    error_time = time.time_ns()

    # 判断是否为CriticalException
    if isinstance(error, CriticalException):
        is_critical_exception: bool = True
    else:
        is_critical_exception: bool = False
    
    error_message = str(error)
    
    if isinstance(error, ValidationError):
        if ConfigManager.get_configs().global_exception_handler.format_validation_error:
            format_text_buffer: list[str] = [
                "Validation Error:"
            ]
            errors = error.errors()
            for detail in errors:
                format_text_buffer.append(
                    f"- [{'.'.join(detail['loc'])}]: {detail['msg']}"
                )
            error_message = "\n".join(format_text_buffer)

    # 记录异常日志
    traceback_info = traceback.format_exc()
    if is_critical_exception:
        logger.critical(
            "Critical Exception: \n{traceback}\n{message}",
            user_id = "[Global Exception Recorder]",
            traceback = traceback_info,
            message = error_message
        )
    else:
        logger.exception(
            "Exception: \n{traceback}\n{message}",
            user_id = "[Global Exception Recorder]",
            traceback = traceback_info,
            message = error_message
        )

    
    # 记录Traceback
    if ConfigManager.get_configs().global_exception_handler.traceback_save_to:
        await save_error_traceback(
            datetime.fromtimestamp(error_time / 1e9),
            traceback_info
        )
    
    # 判断是否要关闭服务器
    if is_critical_exception:
        if ConfigManager.get_configs().global_exception_handler.crash_exit:
            asyncio.create_task(shutdown_server(error))
        else:
            logger.critical(
                "A critical error has occurred on the server, but the server has not been allowed to go down!",
                user_id = "[Global Exception Recorder]",
            )
    
    error_response = ErrorResponse(
        error_code = 500,
        source_exception = type(error).__name__,
        exception_message = str(error)
    )
    if is_critical_exception:
        error_response.error_message = ConfigManager.get_configs().global_exception_handler.critical_error_message
    else:
        error_response.error_message = ConfigManager.get_configs().global_exception_handler.error_message
    
    if ConfigManager.get_configs().global_exception_handler.error_output_include_traceback:
        error_response.exception_traceback = traceback_info

    return ORJSONResponse(
        status_code=error_response.error_code,
        content=error_response.model_dump(exclude_none=True)
    )