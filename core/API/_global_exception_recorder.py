from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import ORJSONResponse
from loguru import logger
import traceback
import asyncio
import time
import signal
import os

from ._resource import app
from ..CriticalException import CriticalException
from ..Global_Config_Manager import ConfigManager

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except CriticalException as e:
        # 记录异常日志
        try:
            traceback_info = traceback.format_exc()
            logger.critical("Critical Exception: \n{traceback}", user_id = "[Global Exception Recorder]", traceback = traceback_info)
        except KeyError:
            logger.exception("Exception: {exception}", exception = e)
        # 触发后台任务关闭应用（非阻塞）
        background_tasks = BackgroundTasks()
        background_tasks.add_task(shutdown_server, exception = e)
        error_time = time.time_ns()
        return ORJSONResponse(
            status_code=500,
            content={
                "message": ConfigManager.get_configs().server.critical_error_message,
                "error": str(e),
                "time": error_time / 1e9,
                "time_ns": error_time,
            },
        )
    except Exception as e:
        # 记录异常日志
        traceback_info = traceback.format_exc()
        logger.exception("An Exception occurred:\n{traceback}", user_id = "[Global Exception Recorder]", traceback = traceback_info)
        error_time = time.time_ns()
        return ORJSONResponse(
            status_code=500,
            content={
                "message": ConfigManager.get_configs().server.error_message,
                "error": str(e),
                "time": error_time / 1e9,
                "time_ns": error_time,
            },
        )

async def shutdown_server(exception: CriticalException | None = None) -> None:
    wait_time: float = 0.0
    if exception is not None:
        if callable(exception.wait):
            try:
                logger.info("Exceptions include waiting callbacks, and programs may exit delayed...", user_id = "[Global Exception Recorder]")
            except KeyError:
                logger.info("[Global Exception Recorder] Exceptions include waiting callbacks, and programs may exit delayed...")
            if asyncio.iscoroutinefunction(exception.wait):
                wait_time = await exception.wait(exception)
            elif callable(exception.wait):
                wait_time: float = await asyncio.to_thread(exception.wait, exception)
            elif not isinstance(wait_time, float):
                wait_time = exception.wait
        elif isinstance(exception.wait, float):
            wait_time: float = exception.wait
    
    if (isinstance(wait_time, float) or isinstance(wait_time, int)) and wait_time > 0:
        try:
            logger.info(f"Waiting for {wait_time} seconds before closing the application...", user_id = "[Global Exception Recorder]")
        except KeyError:
            logger.info("[Global Exception Recorder] Waiting for {wait_time} seconds before closing the application...")
        await asyncio.sleep(wait_time)

    logger.critical("正在关闭应用...")
    # 发送 SIGTERM 信号终止进程
    os.kill(os.getpid(), signal.SIGTERM)