# ==== 标准库 ==== #
from __future__ import annotations

# ==== 第三方库 ==== #
from loguru import logger

# ==== 自定义库 ==== #
from ..auxiliary.time import print_init_runtime
from ..global_config_manager import ConfigManager
from ._server import Server

class ServerIniter:
    def __init__(
        self,
        server: Server,
    ) -> None:
        self.server = server

    def inited(self):
        return self.server.inited()

    def init_all(self):
        self.init_runtime()
        self.init_core()
        self.init_routers()
        self.init_admin_key_manager()
    
    def init_middleware(self):
        from ._http_middleware import middleware_factory
        middleware_factory(
            self.server.app,
            server = self.server.server,
        )
    
    def init_logger(self):
        from ..logger_init import logger_init
        # 初始化日志
        logger_init(
            ConfigManager.get_configs().logger,
        )
        logger.info("Logger has been initialized.")
        self.server._logger_inited = True
    
    @print_init_runtime("Runtime")
    def init_runtime(self):
        from ..runtime_container import RuntimeContainer
        self.server.runtime = RuntimeContainer.init_runtime()
    
    @print_init_runtime("Core")
    def init_core(self):
        from ..core import Core
        self.server.core = Core(
            runtime = self.server.runtime
        )
    
    @print_init_runtime("Routers")
    def init_routers(self):
        from ..api import root_router
        self.server.app.include_router(
            root_router
        )
    
    @print_init_runtime("Admin Key Manager")
    def init_admin_key_manager(self):
        from ..admin_api_key_manager import AdminKeyManager
        self.server.admin_key_manager = AdminKeyManager()
    
    @print_init_runtime("Server")
    def init_server(
        self,
        host: str,
        port: int,
        workers: int = 1,
        reload: bool = False
    ):
        from uvicorn import Server, Config
        # 初始化API
        self.server.server = Server(
            Config(
                app = self.server.app,
                host = host,
                port = port,
                workers = workers,
                reload = reload,
                log_config = None
            )
        )