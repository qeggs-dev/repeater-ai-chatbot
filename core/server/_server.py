# ==== 标准库 ==== #
from __future__ import annotations
import inspect

from typing import (
    ClassVar,
    Sequence,
    Callable,
    Awaitable,
    Any
)

# ==== 第三方库 ==== #
import uvicorn
from fastapi import FastAPI
from loguru import logger

# ==== 自定义库 ==== #
from ..auxiliary.time import print_init_runtime
from ..admin_api_key_manager import AdminKeyManager
from ..core import Core
from ..global_config_manager import ConfigManager
from ..logger_init import logger_init
from ._lifespan import Lifespan
from .._info import __version__
from ..runtime_container import RuntimeContainer

class Server:
    
    def __init__(
        self,
        startup: Sequence[Callable[[], Any]] | None = None,
        shutdown: Sequence[Callable[[], Any]] | None = None
    ) -> None:
        self.app: FastAPI = FastAPI(
            title = "Repeater Chat Backend",
            lifespan = Lifespan,
            on_startup = startup,
            on_shutdown = shutdown,
            version = __version__
        )
        self.server: uvicorn.Server | None = None
        self.keyboard_interrupt_callback: Callable[[], Awaitable[None] | None] = lambda: logger.info("Keyboard interrupt")
        self.admin_key_manager: AdminKeyManager | None = None
    
    core: ClassVar[Core | None] = None
    _logger_inited: ClassVar[bool] = False
    _instance: ClassVar[Server | None] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
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
        ]
        for item in check_list:
            if item is None:
                return False
        return True

    def init_all(self):
        self.init_runtime()
        self.init_core()
        self.init_admin_key_manager()
    
    @classmethod
    def init_logger(cls):
        # 初始化日志
        logger_init(
            ConfigManager.get_configs().logger,
        )
        logger.info("Logger has been initialized.")
        cls._logger_inited = True
    
    @classmethod
    @print_init_runtime("Runtime")
    def init_runtime(cls):
        RuntimeContainer.init_runtime()
    
    @classmethod
    @print_init_runtime("Core")
    def init_core(cls):
        cls.core = Core(runtime = RuntimeContainer.get_runtime())

    @print_init_runtime("Admin Key Manager")
    def init_admin_key_manager(self):
        # 生成或读取API Key
        self.admin_key_manager = AdminKeyManager()
    
    @print_init_runtime("Server")
    def init_server(
        self,
        host: str,
        port: int,
        workers: int = 1,
        reload: bool = False
    ):
        # 初始化API
        self.server = uvicorn.Server(
            uvicorn.Config(
                app = self.app,
                host = host,
                port = port,
                workers = workers,
                reload = reload,
                log_config = None
            )
        )

    async def run_server(self) -> None:
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