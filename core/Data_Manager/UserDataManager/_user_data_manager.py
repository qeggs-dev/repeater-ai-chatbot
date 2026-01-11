
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
            branches_dir_name = ConfigManager.get_configs().user_data.branches_dir_name
        )
    
    async def load(self, user_id: str, default: list = []):
        value = await super().load(user_id, default if isinstance(default, list) else [])
        if not isinstance(value, list):
            raise TypeError("value must be a list")
        return value
    
    async def save(self, user_id: str, data: list):
        if not isinstance(data, list):
            raise TypeError("data must be a list")
        await super().save(user_id, data if isinstance(data, list) else [])

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
            branches_dir_name = ConfigManager.get_configs().user_data.branches_dir_name
        )
    
    async def load(self, user_id: str, default: str = ""):
        value = await super().load(user_id, default if isinstance(default, str) else "")
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        return value
    
    async def save(self, user_id: str, data: str):
        if not isinstance(data, str):
            raise TypeError("data must be a string")
        await super().save(user_id, data if isinstance(data, str) else "")

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
            branches_dir_name = ConfigManager.get_configs().user_data.branches_dir_name
        )
    
    async def load(self, user_id: str, default: dict = {}):
        value = await super().load(user_id, default if isinstance(default, dict) else {})
        if not isinstance(value, dict):
            raise TypeError("value must be a dict")
        return value
    
    async def save(self, user_id: str, data: dict):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        await super().save(user_id, data if isinstance(data, dict) else {})