import sys
import uvicorn

from environs import Env
from core import (
    Global_Config_Manager,
    API as Core_API,
    __version__ as core_version,
    __api_version__ as core_api_version,
)
from loguru import logger

def main():
    env = Env()
    env.read_env()
    config_loader = Global_Config_Manager.ConfigManager()
    config_loader.update_base_path(
        env.path("CONFIG_DIR", "./configs/project_configs"),
        env.json("CONFIG_FORCE_LOAD_LIST", None)
    )
    config_loader.load(
        create_if_missing=True
    )
    Core_API.Resource.init_all()

    host = "0.0.0.0" # 默认监听所有地址
    port = 8000 # 默认监听8000端口

    env_config_host = env.str("HOST", host)
    env_config_port = env.int("PORT", port)
    env_config_workers = env.int("WORKERS", None)
    env_config_reload = env.bool("RELOAD", False)

    host: str | None = Global_Config_Manager.ConfigManager.get_configs().server.host
    if host is None:
        host: str = env_config_host
    
    port: int | None = Global_Config_Manager.ConfigManager.get_configs().server.port
    if port is None:
        port: int = env_config_port
    
    workers: int | None = Global_Config_Manager.ConfigManager.get_configs().server.workers
    if workers is None:
        workers: int = env_config_workers
    
    reload: bool | None = Global_Config_Manager.ConfigManager.get_configs().server.reload
    if reload is None:
        reload: bool = env_config_reload
    
    run_server: bool = Global_Config_Manager.ConfigManager.get_configs().server.run_server

    logger.info(f"Starting server at {host}:{port}")

    if workers:
        logger.info(f"Server will run with {workers} workers")
    
    if reload:
        logger.info("Server will reload on code change")
    
    logger.info(f"Run With Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    logger.info(f"Core Version: {core_version}")
    logger.info(f"Core API Version: {core_api_version}")
    

    if run_server:
        logger.info("Server starting...")
        Core_API.Resource.run_server(
            host = host,
            port = port,
            workers = workers,
            reload = reload
        )
    else:
        logger.warning("Server startup is disabled.")

if __name__ == "__main__":
    main()