
from ._main_user_data_manager import MainManager as UserDataManager
from ...Global_Config_Manager import ConfigManager, Cache_Data_Config

class ContextManager(UserDataManager[list]):
    def __init__(self):
        super().__init__(
            "Context_UserData",
            cache_metadata = (
                ConfigManager.get_configs().user_data.cache_medadata.context
                if isinstance(ConfigManager.get_configs().user_data.cache_medadata, Cache_Data_Config)
                else ConfigManager.get_configs().user_data.cache_medadata
            ),
            cache_data = (
                ConfigManager.get_configs().user_data.cache_data.context
                if isinstance(ConfigManager.get_configs().user_data.cache_data, Cache_Data_Config)
                else ConfigManager.get_configs().user_data.cache_data
            ),
            branches_dir_name = ConfigManager.get_configs().user_data.branches_dir_name,
            default_factory = list
        )

class PromptManager(UserDataManager[str]):
    def __init__(self):
        super().__init__(
            "Prompt_UserData",
            cache_metadata = (
                ConfigManager.get_configs().user_data.cache_medadata.prompt
                if isinstance(ConfigManager.get_configs().user_data.cache_medadata, Cache_Data_Config)
                else ConfigManager.get_configs().user_data.cache_medadata
            ),
            cache_data = (
                ConfigManager.get_configs().user_data.cache_data.prompt
                if isinstance(ConfigManager.get_configs().user_data.cache_data, Cache_Data_Config)
                else ConfigManager.get_configs().user_data.cache_data
            ),
            branches_dir_name = ConfigManager.get_configs().user_data.branches_dir_name,
            default_factory = lambda: ""
        )

class UserConfigManager(UserDataManager[dict]):
    def __init__(self):
        super().__init__(
            "UserConfig_UserData",
            cache_metadata = (
                ConfigManager.get_configs().user_data.cache_medadata.config
                if isinstance(ConfigManager.get_configs().user_data.cache_medadata, Cache_Data_Config)
                else ConfigManager.get_configs().user_data.cache_medadata
            ),
            cache_data = (
                ConfigManager.get_configs().user_data.cache_data.config
                if isinstance(ConfigManager.get_configs().user_data.cache_data, Cache_Data_Config)
                else ConfigManager.get_configs().user_data.cache_data
            ),
            branches_dir_name = ConfigManager.get_configs().user_data.branches_dir_name,
            default_factory = lambda: {}
        )