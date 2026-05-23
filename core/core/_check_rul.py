from ..user_config_manager import UserConfigs
from ..global_config_manager import GlobalConfigs

def check_rul(
    configs: UserConfigs,
    global_configs: GlobalConfigs,
    save_context: bool | None = None,
) -> bool:
    if save_context is None:
        save_context = configs.save_context
    if save_context is None:
        save_context = global_configs.context.save_context
    
    return save_context