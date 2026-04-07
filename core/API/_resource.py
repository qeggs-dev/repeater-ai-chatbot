# ==== 标准库 ==== #
from __future__ import annotations

from typing import ClassVar, Sequence, Callable, Any

# ==== 第三方库 ==== #
import uvicorn

from fastapi import FastAPI

# ==== 自定义库 ==== #
from AdminApikeyManager import AdminKeyManager
from RegexChecker import RegexChecker
from .._core import Core
from ..Global_Config_Manager import ConfigManager
from ..Pools.awaitable_pool import TaskPool
from ..Markdown_Render import HTMLRenderClient
from ..Logger_Init import logger_init
from ._lifespan import lifespan
from ._info import __version__
from ..Licenses_Loader import LicenseLoader
from ..Nexus_Client import NexusClient

class Resource:
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
    chat_task_pool: ClassVar[TaskPool] = TaskPool()
    admin_key_manager: ClassVar[AdminKeyManager | None] = None
    html_render_client: ClassVar[HTMLRenderClient | None] = None
    nexus_client: ClassVar[NexusClient | None] = None
    licenses: ClassVar[LicenseLoader | None] = None
    _instance: ClassVar[Resource | None] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def inited(cls):
        check_list: list[Any | None] = [
            cls.core,
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
        cls.init_logger()
        cls.init_core()
        cls.init_nexus_client()
        cls.init_licenses_data()
        cls.init_admin_key_manager()
        cls.init_browser_pool_manager()
    
    @classmethod
    def init_core(cls):
        cls.core = Core()
    
    @classmethod
    def init_logger(cls):
        # 初始化日志
        logger_init(
            ConfigManager.get_configs().logger,
        )

    @classmethod
    def init_admin_key_manager(cls):
        # 生成或读取API Key
        cls.admin_key_manager = AdminKeyManager()
    
    @classmethod
    def init_licenses_data(cls):
        cls.licenses = LicenseLoader(ConfigManager.get_configs().licenses)
        cls.licenses.scan_licenses()
    
    @classmethod
    def init_nexus_client(cls):
        cls.nexus_client = NexusClient(
            base_url = ConfigManager.get_configs().nexus.base_url,
            request_timeout = ConfigManager.get_configs().nexus.api_timeout,
        )

    @classmethod
    def init_browser_pool_manager(cls):
        # 渲染配置
        render_config = ConfigManager.get_configs().render
        cls.html_render_client = HTMLRenderClient(
            base_url = render_config.to_image.base_url,
            timeout = render_config.to_image.timeout
        )

    @classmethod
    def run_server(
        cls,
        host: str,
        port: int,
        workers: int = 1,
        reload: bool = False
    ) -> None:
        if not cls.inited():
            raise RuntimeError("API not initialized")
        uvicorn.run(
            app = cls.app,
            host = host,
            port = port,
            workers = workers,
            reload = reload,
            log_config = None,
        )