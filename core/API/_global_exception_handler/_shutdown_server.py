from loguru import logger
import asyncio
import inspect
import signal
import os

from ...SpecialException import CriticalException

async def shutdown_server(exception: CriticalException | None = None, use_sigterm: bool = False) -> None:
    wait_time: float = 0.0
    if isinstance(exception, CriticalException):
        if callable(exception.wait):
            try:
                logger.info(
                    "Exceptions include waiting callbacks, and programs may exit delayed...",
                    user_id = "[Global Exception Recorder]"
                )
            except KeyError:
                logger.info(
                    "Exceptions include waiting callbacks, and programs may exit delayed..."
                )
            
            if inspect.iscoroutinefunction(exception.wait):
                wait_time = await exception.wait(exception)
            elif callable(exception.wait):
                wait_time: float = await asyncio.to_thread(exception.wait, exception)
            elif not isinstance(wait_time, float):
                wait_time = exception.wait
            else:
                try:
                    logger.error(
                        "The wait handler is invalid.",
                        user_id = "[Global Exception Recorder]",
                    )
                except KeyError:
                    logger.error(
                        "The wait handler is invalid.",
                    )
        elif isinstance(exception.wait, float):
            wait_time: float = exception.wait
    
    if (isinstance(wait_time, float) or isinstance(wait_time, int)) and wait_time > 0:
        try:
            logger.info(
                "Waiting for {wait_time} seconds before closing the application...",
                user_id = "[Global Exception Recorder]",
                wait_time = wait_time
            )
        except KeyError:
            logger.info(
                "Waiting for {wait_time} seconds before closing the application...",
                wait_time = wait_time
            )
        await asyncio.sleep(wait_time)

    logger.critical("The server crashed! exiting...")
    if use_sigterm:
        # 发送 SIGTERM 信号，这会让程序直接退出
        os.kill(os.getpid(), signal.SIGTERM)
    else:
        # 发送 SIGINT 信号，因为这会触发 KeyboardInterrupt 并让程序正常退出，保证资源正常关闭
        os.kill(os.getpid(), signal.SIGINT)