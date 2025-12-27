from loguru import logger
import asyncio
import signal
import os

from ...CriticalException import CriticalException

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

    logger.critical("The server crashed! exiting...")
    # 发送 SIGTERM 信号终止进程
    os.kill(os.getpid(), signal.SIGTERM)