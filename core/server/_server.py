# ==== 标准库 ==== #
from __future__ import annotations
import inspect
import time

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
    startup: ClassVar[Sequence[Callable[[], Any]] | None] = None
    shutdown: ClassVar[Sequence[Callable[[], Any]]] | None = None
    
    app: ClassVar[FastAPI] = FastAPI(
        title = "RepeaterChatBackend",
        lifespan = Lifespan,
        on_startup = startup,
        on_shutdown = shutdown,
        version = __version__
    )
    core: ClassVar[Core | None] = None
    server: ClassVar[uvicorn.Server | None] = None
    keyboard_interrupt_callback: ClassVar[Callable[[], Awaitable[None] | None]] = None
    admin_key_manager: ClassVar[AdminKeyManager | None] = None
    _logger_inited: ClassVar[bool] = False
    _instance: ClassVar[Server | None] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def logger_inited(self):
        return self._logger_inited

    @classmethod
    def inited(cls):
        if not cls._logger_inited:
            return False
        check_list: list[Any | None] = [
            cls.core,
            cls.server,
            cls.admin_key_manager,
        ]
        for item in check_list:
            if item is None:
                return False
        return True

    @classmethod
    def init_all(cls):
        cls.init_runtime()
        cls.init_core()
        cls.init_admin_key_manager()
    
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

    @classmethod
    @print_init_runtime("Admin Key Manager")
    def init_admin_key_manager(cls):
        # 生成或读取API Key
        cls.admin_key_manager = AdminKeyManager()
    
    @classmethod
    @print_init_runtime("Server")
    def init_server(
        cls,
        host: str,
        port: int,
        workers: int = 1,
        reload: bool = False
    ):
        # 初始化API
        cls.server = uvicorn.Server(
            uvicorn.Config(
                app = cls.app,
                host = host,
                port = port,
                workers = workers,
                reload = reload,
                log_config = None
            )
        )

    @classmethod
    async def run_server(
        cls
    ) -> None:
        if not cls.inited():
            raise RuntimeError("API not initialized")
        try:
            await cls.server.serve()
        except KeyboardInterrupt:
            if cls.keyboard_interrupt_callback:
                if inspect.iscoroutinefunction(cls.keyboard_interrupt_callback):
                    await cls.keyboard_interrupt_callback()
                else:
                    cls.keyboard_interrupt_callback()
            await cls.server.shutdown()
        except Exception as e:
            logger.error(f"Server error: {e}")