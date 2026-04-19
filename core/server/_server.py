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

# ==== 自定义库 ==== #
from ..admin_api_key_manager import AdminKeyManager
from ..auxiliary.regex_checker import RegexChecker
from .._core import Core
from ..global_config_manager import ConfigManager
from ..pools.awaitable_pool import TaskPool
from ..markdown_render import HTMLRenderClient
from ..logger_init import logger_init
from ._lifespan import lifespan
from .._info import __version__
from ..licenses_loader import LicenseLoader
from ..nexus_client import NexusClient
from loguru import logger

class Server:
    startup: ClassVar[Sequence[Callable[[], Any]] | None] = None
    shutdown: ClassVar[Sequence[Callable[[], Any]]] | None = None
    
    app: ClassVar[FastAPI] = FastAPI(
        title = "RepeaterChatBackend",
        lifespan = lifespan,
        on_startup = startup,
        on_shutdown = shutdown,
        version = __version__
    )
    core: ClassVar[Core | None] = None
    server: ClassVar[uvicorn.Server | None] = None
    keyboard_interrupt_callback: ClassVar[Callable[[], Awaitable[None] | None]] = None
    chat_task_pool: ClassVar[TaskPool] = TaskPool()
    admin_key_manager: ClassVar[AdminKeyManager | None] = None
    html_render_client: ClassVar[HTMLRenderClient | None] = None
    nexus_client: ClassVar[NexusClient | None] = None
    licenses: ClassVar[LicenseLoader | None] = None
    _instance: ClassVar[Server | None] = None

    class _InitializingTimer:
        def __init__(
            self,
            name: str,
        ):
            self._enter_time: int = 0
            self._exit_time: int = 0
            self._task_name: str = name
        
        def __enter__(self) -> None:
            logger.info(
                "Initializing {name}...",
                name = self._task_name
            )
            self._enter_time = time.perf_counter_ns()

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            self._exit_time = time.perf_counter_ns()
            logger.info(
                "Initialized {name} in {initialize_time:.3f} ms.",
                name = self._task_name,
                initialize_time = (self._exit_time - self._enter_time) / 1e6
            )

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def inited(cls):
        check_list: list[Any | None] = [
            cls.core,
            cls.server,
            cls.admin_key_manager,
            cls.html_render_client,
            cls.nexus_client,
            cls.licenses,
        ]
        for item in check_list:
            if item is None:
                return False
        return True

    @classmethod
    def init_all(cls):
        cls.init_core()
        cls.init_nexus_client()
        cls.init_licenses_data()
        cls.init_admin_key_manager()
        cls.init_html_render_client()
    
    @classmethod
    def init_core(cls):
        with cls._InitializingTimer("Core"):
            cls.core = Core()
    
    @classmethod
    def init_logger(cls):
        # 初始化日志
        logger_init(
            ConfigManager.get_configs().logger,
        )
        logger.info("Logger has been initialized.")

    @classmethod
    def init_admin_key_manager(cls):
        with cls._InitializingTimer("Admin Key Manager"):
            # 生成或读取API Key
            cls.admin_key_manager = AdminKeyManager()
    
    @classmethod
    def init_licenses_data(cls):
        with cls._InitializingTimer("Licenses Data"):
            cls.licenses = LicenseLoader(ConfigManager.get_configs().licenses)
            cls.licenses.scan_licenses()
    
    @classmethod
    def init_nexus_client(cls):
        with cls._InitializingTimer("Nexus Client"):
            cls.nexus_client = NexusClient(
                base_url = ConfigManager.get_configs().nexus.base_url,
                request_timeout = ConfigManager.get_configs().nexus.api_timeout,
            )

    @classmethod
    def init_html_render_client(cls):
        with cls._InitializingTimer("HTML Render Client"):
            # 渲染配置
            render_config = ConfigManager.get_configs().render
            cls.html_render_client = HTMLRenderClient(
                base_url = render_config.to_image.base_url,
                timeout = render_config.to_image.timeout
            )
    
    @classmethod
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