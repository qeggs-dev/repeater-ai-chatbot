import time
start_import_time = time.perf_counter_ns()
import sys
import asyncio

from environs import Env
from core import (
    global_config_manager,
    Server,
    __version__ as core_version,
    requirements_version_checker
)
from loguru import logger
end_import_time = time.perf_counter_ns()

class RepeaterMain:
    env = Env()
    env.read_env()

    def load_configs(self):
        config_loader = global_config_manager.ConfigManager()
        config_loader.update_base_path(
            self.env.path("CONFIG_DIR", "./configs/project_configs"),
            self.env.json("CONFIG_FORCE_LOAD_LIST", None)
        )
        config_loader.load(
            create_if_missing=True
        )
    
    def init_server(self):
        host = "0.0.0.0" # 默认监听所有地址
        port = 8000 # 默认监听8000端口

        env_config_host = self.env.str("HOST", host)
        env_config_port = self.env.int("PORT", port)
        env_config_workers = self.env.int("WORKERS", None)
        env_config_reload = self.env.bool("RELOAD", False)

        host: str | None = global_config_manager.ConfigManager.get_configs().server.host
        if host is None:
            host: str = env_config_host
        
        port: int | None = global_config_manager.ConfigManager.get_configs().server.port
        if port is None:
            port: int = env_config_port
        
        workers: int | None = global_config_manager.ConfigManager.get_configs().server.workers
        if workers is None:
            workers: int = env_config_workers
        
        reload: bool | None = global_config_manager.ConfigManager.get_configs().server.reload
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
    
    def check_package(self):
        logger.info("Checking Packages...")
        start_check_packages_time = time.perf_counter_ns()
        requirements_version_checker.check_package_list(
            strict_mode = global_config_manager.ConfigManager.get_configs().requirements.strict_mode
        )
        end_check_packages_time = time.perf_counter_ns()
        logger.info(
            "Check Packages Time: {check_packages_time:.2f}ms",
            check_packages_time = (end_check_packages_time - start_check_packages_time) / 1e6
        )
    
    def init_all(self):
        start_load_configs_time = time.perf_counter_ns()
        self.load_configs()
        end_load_configs_time = time.perf_counter_ns()
        Server.init_logger()

        logger.info(
            "Import Packages Time: {import_packages_time:.2f}ms",
            import_packages_time = (end_import_time - start_import_time) / 1e6
        )

        logger.info(
            "Load Configs Time: {load_configs_time:.2f}ms",
            load_configs_time = (end_load_configs_time - start_load_configs_time) / 1e6
        )
        
        logger.info(f"Run With Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        logger.info(f"Core Version: {core_version}")

        if global_config_manager.ConfigManager.get_configs().requirements.enable_check:
            self.check_package()

        start_init_resource_time = time.perf_counter_ns()
        Server.init_all()
        end_init_resource_time = time.perf_counter_ns()

        logger.info(
            "Init Server Time: {init_resource_time:.2f}ms",
            init_resource_time = (end_init_resource_time - start_init_resource_time) / 1e6
        )

    def run(self):
        logger.info("Server starting...")
        try:
            asyncio.run(
                Server.run_server()
            )
        except KeyboardInterrupt:
            logger.info("Server shutting down...")

def main(run_server: bool | None = None):
    repeater_main = RepeaterMain()
    if run_server is None:
        run_server = global_config_manager.ConfigManager.get_configs().server.run_server
    
    repeater_main.init_all()
    repeater_main.init_server()
    
    if run_server:
        repeater_main.run()

if __name__ == "__main__":
    main()