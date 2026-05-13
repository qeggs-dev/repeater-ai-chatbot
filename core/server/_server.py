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

    async def run_server(self) -> None:
        async with self.lifespan:
            if not self.inited():
                raise RuntimeError("API not initialized")
            try:
                await self.server.serve()
            except KeyboardInterrupt:
                if self.keyboard_interrupt_callback:
                    if inspect.iscoroutinefunction(self.keyboard_interrupt_callback):
                        await self.keyboard_interrupt_callback()
                    else:
                        self.keyboard_interrupt_callback()
                await self.server.shutdown()
            except Exception as e:
                logger.error(f"Server error: {e}")