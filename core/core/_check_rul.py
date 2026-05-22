import asyncio
from loguru import logger
from ._empty_async_context_manager import EmptyAsyncContextManager
from ..user_config_manager import UserConfigs
from ..global_config_manager import GlobalConfigs

def check_rul(
    rul: asyncio.Lock,
    configs: UserConfigs,
    global_configs: GlobalConfigs,
    save_context: bool | None = None,
):
    if save_context is None:
        save_context = configs.save_context
    if save_context is None:
        save_context = global_configs.context.save_context
    
    if save_context:
        logger.info(
            "RUL is Enabled."
        )
        return rul
    else:
        logger.warning(
            "RUL is Disabled."
        )
        return EmptyAsyncContextManager()