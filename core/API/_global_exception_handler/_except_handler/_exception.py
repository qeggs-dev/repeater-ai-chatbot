import sys
import time
import asyncio
import traceback

from pathlib import Path
from loguru import logger
from datetime import datetime
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError

from ....CriticalException import CriticalException
from ....Global_Config_Manager import ConfigManager
from .._shutdown_server import shutdown_server
from .._save_error_traceback import save_error_traceback
from .._error_output_model import ErrorResponse
from .._get_code import get_code_async

async def exception_handler(error: BaseException) -> None:
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
    
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_info: traceback.StackSummary = traceback.extract_tb(exc_traceback)
    last_tb = traceback_info[-1]
    raiser_file = Path(last_tb.filename)

    if ConfigManager.get_configs().global_exception_handler.code_reader.enable:
        if raiser_file.exists() and raiser_file.is_file() and last_tb.lineno is not None and last_tb.lineno > 0:
            code = await get_code_async(raiser_file, last_tb.lineno)
        else:
            code = "[Invalid Code Frame]"
    else:
        code = "[Code Reader Disabled]"

    # 记录异常日志
    traceback_str = traceback.format_exc()
    if is_critical_exception:
        logger.critical(
            (
                "Critical Exception:\n"
                "{error_name}\n"
                "    - Depth of stack frame:\n"
                "        {total_tb_count}\n"
                "    - Raised from:\n"
                "        {raiser}\n"
                "    - Message: \n"
                "        {message}\n"
                "    - Traceback: \n"
                "        {traceback}\n"
                "File: \n"
                "{code}"
            ),
            user_id = "[Global Exception Recorder]",
            total_tb_count = len(traceback_info),
            raiser = raiser_file.as_posix(),
            lineno = last_tb.lineno,
            error_name = error.__class__.__name__,
            message = error_message.replace("\n", "\n        "),
            traceback = traceback_str.replace("\n", "\n        "),
            code = code
        )
    else:
        logger.exception(
            (
                "Exception: \n"
                "{error_name}\n"
                "    - Depth of stack frame:\n"
                "        {total_tb_count}\n"
                "    - Raised from:\n"
                "        {raiser}:{lineno}\n"
                "    - Message: \n"
                "        {message}\n"
                "    - Traceback: \n"
                "        {traceback}\n"
                "File: \n"
                "{code}"
            ),
            user_id = "[Global Exception Recorder]",
            total_tb_count = len(traceback_info),
            raiser = raiser_file.as_posix(),
            lineno = last_tb.lineno,
            error_name = error.__class__.__name__,
            message = error_message.replace("\n", "\n        "),
            traceback = traceback_str.replace("\n", "\n        "),
            code = code
        )

    
    # 记录Traceback
    if ConfigManager.get_configs().global_exception_handler.traceback_save_to:
        await save_error_traceback(
            datetime.fromtimestamp(error_time / 1e9),
            traceback_str
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
        error_response.exception_traceback = traceback_str

    return ORJSONResponse(
        status_code=error_response.error_code,
        content=error_response.model_dump(exclude_none=True)
    )