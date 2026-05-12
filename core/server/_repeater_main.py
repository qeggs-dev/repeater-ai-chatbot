import time
import sys
import asyncio

from environs import Env
from ..global_config_manager import (
    ConfigManager,
    GlobalConfigs,       
)
from ..server import Server
from .._info import __version__
from ..requirements_version_checker import check_package_list
from loguru import logger

class RepeaterMain:
    env = Env()
    env.read_env()

    def load_configs(self):
        config_loader = ConfigManager()
        config_loader.update_base_path(
            self.env.path("CONFIG_DIR", "./configs/project_configs"),
            self.env.json("CONFIG_FORCE_LOAD_LIST", None)
        )
        return config_loader.load(
            create_if_missing=True
        )
    
    def init_server(self, configs: GlobalConfigs):
        host = "0.0.0.0" # 默认监听所有地址
        port = 8000 # 默认监听8000端口

        env_config_host = self.env.str("HOST", host)
        env_config_port = self.env.int("PORT", port)
        env_config_workers = self.env.int("WORKERS", None)
        env_config_reload = self.env.bool("RELOAD", False)

        host: str | None = configs.server.host
        if host is None:
            host: str = env_config_host
        
        port: int | None = configs.server.port
        if port is None:
            port: int = env_config_port
        
        workers: int | None = configs.server.workers
        if workers is None:
            workers: int = env_config_workers
        
        reload: bool | None = configs.server.reload
        if reload is None:
            reload: bool = env_config_reload

        logger.info(f"Starting server at {host}:{port}")

        if workers:
            logger.info(f"Server will run with {workers} workers")
        
        if reload:
            logger.info("Server will reload on code change")
        
        Server.init_server(
            host = host,
            port = port,
            workers = workers,
            reload = reload
        )
    
    def check_package(self, configs: GlobalConfigs):
        logger.info("Checking Packages...")
        start_check_packages_time = time.perf_counter_ns()
        check_package_list(
            strict_mode = configs.requirements.strict_mode
        )
        end_check_packages_time = time.perf_counter_ns()
        logger.info(
            "Check Packages Time: {check_packages_time:.2f}ms",
            check_packages_time = (end_check_packages_time - start_check_packages_time) / 1e6
        )
    
    @staticmethod
    def init_logger():
        Server.init_logger()
    
    
    def init_all(self, configs: GlobalConfigs):
        logger.info(f"Run With Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        logger.info(f"Core Version: {__version__}")

        if configs.requirements.enable_check:
            self.check_package(configs)

        start_init_resource_time = time.perf_counter_ns()
        Server.init_all()
        end_init_resource_time = time.perf_counter_ns()

        logger.info(
            "Init Server Time: {init_resource_time:.2f}ms",
            init_resource_time = (end_init_resource_time - start_init_resource_time) / 1e6
        )
    
    async def run_server(self):
        await Server.run_server()

    def run(self):
        logger.info("Server starting...")
        try:
            asyncio.run(
                self.run_server()
            )
        except KeyboardInterrupt:
            logger.info("Server shutting down...")
        except Exception as e:
            logger.exception(e)