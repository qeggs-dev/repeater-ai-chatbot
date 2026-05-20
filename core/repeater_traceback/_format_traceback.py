import time
import asyncio
import traceback

from loguru import logger
from datetime import datetime
from uvicorn import Server
from fastapi.responses import ORJSONResponse

from ..special_exception import CriticalException, HTTPException
from ..global_config_manager import ConfigManager
from ._shutdown_server import shutdown_server
from ._save_error_traceback import save_error_traceback
from ._error_output_model import ErrorResponse
from ._traceback import TracebackHandler

async def log_traceback(error: BaseException, server: Server) -> ORJSONResponse:
    error_time = time.time_ns()

    error_code = 500
    exception_message = str(error)
    extra_data = None

    configs = ConfigManager.get_configs()

    # 判断是否为特殊Exception
    is_critical_exception: bool = isinstance(error, CriticalException)
    is_http_exception: bool = isinstance(error, HTTPException)

    if configs.global_exception_handler.repeater_traceback.enable:
        repeater_traceback = TracebackHandler()
        traceback_str = await repeater_traceback.format_traceback(
            time.strftime(
                configs.global_exception_handler.repeater_traceback.timeformat,
                time.localtime(error_time / 1e9)
            ),
            configs.global_exception_handler.repeater_traceback.exclude_library_code,
            configs.global_exception_handler.code_reader.enable,
            configs.global_exception_handler.repeater_traceback.traditional_stack_frame,
            configs.global_exception_handler.repeater_traceback.format_validation_error
        )
    else:
        traceback_str = traceback.format_exc()
    
    # 写入 HTTP 状态码
    if is_http_exception:
        error_code = error.status_code

    # 记录异常日志
    log_template = [
        "{prompt}: {message}"
    ]
    if is_critical_exception:
        prompt = "CriticalException"
        log_func = logger.critical
        log_template.append("{traceback}")
    elif is_http_exception:
        prompt = "HTTPException"
        if 500 <= error_code < 600:
            log_func = logger.error
            log_template.append("{traceback}")
        else:
            log_func = logger.warning
            if configs.global_exception_handler.record_warn_http_exception:
                log_template.append("{traceback}")
    else:
        prompt = "Exception"
        log_func = logger.exception
        log_template.append("{traceback}")
    
    log_func(
        "\n".join(log_template),
        prompt = prompt,
        user_id = "[Global Exception Recorder]",
        traceback = traceback_str
    )
        

    # 记录Traceback
    if configs.global_exception_handler.traceback_save_to:
        await save_error_traceback(
            datetime.fromtimestamp(error_time / 1e9),
            traceback_str
        )
    
    # 判断是否要关闭服务器
    if is_critical_exception:
        if configs.global_exception_handler.crash_exit:
            asyncio.create_task(
                shutdown_server(
                    server = server,
                    exception = error,
                )
            )
        else:
            logger.critical(
                "A critical error has occurred on the server, but the server has not been allowed to go down!",
                user_id = "[Global Exception Recorder]",
            )
    
    error_response = ErrorResponse(
        error_code = error_code,
        timestamp_ns = error_time,
        unix_timestamp = error_time // 1_000_000_000,
        source_exception = type(error).__name__,
        exception_message = exception_message,
        extra_body = extra_data
    )
    if is_critical_exception:
        error_response.error_message = configs.global_exception_handler.critical_error_message
    elif is_http_exception:
        error_response.error_message = error.message
    else:
        error_response.error_message = configs.global_exception_handler.error_message
    
    if configs.global_exception_handler.error_output_include_traceback:
        error_response.exception_traceback = traceback_str

    return ORJSONResponse(
        status_code = error_response.error_code,
        content = error_response.model_dump(exclude_none=True)
    )