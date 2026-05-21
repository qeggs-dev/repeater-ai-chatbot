# ==== 标准库 ==== #
from __future__ import annotations
import inspect
import asyncio

from typing import (
    ClassVar,
    Sequence,
    AsyncContextManager,
    Callable,
    Awaitable,
    Any
)

# ==== 第三方库 ==== #
import uvicorn
from fastapi import FastAPI
from loguru import logger

# ==== 自定义库 ==== #
from ..admin_api_key_manager import AdminKeyManager
from ..core import Core
from ._lifespan import Lifespan
from .._info import __version__
from ..runtime_container import RepeaterRuntime

class Server:
    _logger_inited: ClassVar[bool] = False

    def __init__(
        self,
        lifespan: AsyncContextManager[None] | None = None,
        startup: Sequence[Callable[[], Any]] | None = None,
        shutdown: Sequence[Callable[[], Any]] | None = None
    ) -> None:
        self.app: FastAPI = FastAPI(
            title = "Repeater Chat Backend",
            on_startup = startup,
            on_shutdown = shutdown,
            version = __version__
        )
        self.runtime: RepeaterRuntime | None = None
        self.server: uvicorn.Server | None = None
        self.lifespan: AsyncContextManager[None] = lifespan
        if self.lifespan is None:
            self.lifespan = Lifespan(self.app)
        self.keyboard_interrupt_callback: Callable[[], Awaitable[None] | None] = lambda: logger.info("Keyboard interrupt")
        self.admin_key_manager: AdminKeyManager | None = None
        self.core: Core | None = None
        self._serve_task: asyncio.Task[None] | None = None
        self._exit_code: int = 0
        self._shutdowned: bool = True
    
    @property
    def exit_code(self) -> int:
        return self._exit_code
    
    async def shutdown(self, exit_code: int = 0) -> None:
        if self._shutdowned:
            return
        await self.server.shutdown()
        self._exit_code = exit_code
        if self._serve_task is not None:
            self._serve_task.cancel()
        self._shutdowned = True
    
    @classmethod
    def logger_inited(self):
        return self._logger_inited

    def inited(self):
        if not self._logger_inited:
            return False
        
        check_list: list[Any | None] = [
            self.core,
            self.server,
            self.admin_key_manager,
            self.runtime
        ]
        for item in check_list:
            if item is None:
                return False
        return True

    async def run_server(self) -> int:
        async with self.lifespan:
            if not self.inited():
                raise RuntimeError("API not initialized")
            self._shutdowned = False
            self._serve_task = asyncio.create_task(
                self.server.serve()
            )
            try:
                await self._serve_task
            except KeyboardInterrupt:
                if self.keyboard_interrupt_callback:
                    if inspect.iscoroutinefunction(self.keyboard_interrupt_callback):
                        await self.keyboard_interrupt_callback()
                    else:
                        self.keyboard_interrupt_callback()
            except asyncio.CancelledError:
                logger.info("Server cancelled")
            except Exception as e:
                logger.error(f"Server error: {e}")
            finally:
                await self.shutdown()
        return self._exit_code