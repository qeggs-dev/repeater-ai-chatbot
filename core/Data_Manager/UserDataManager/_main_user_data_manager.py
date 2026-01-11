# ==== 标准库 ==== #
from typing import Any
from pathlib import Path
from weakref import WeakValueDictionary

# ==== 第三方库 ==== #
from loguru import logger

# ==== 自定义库 ==== #
from .SubManager import SubManager
from PathProcessors import validate_path, sanitize_filename
from ...Global_Config_Manager import ConfigManager

class MainManager:
    def __init__(self, base_name: str, cache_metadata:bool = False, cache_data:bool = False, branches_dir_name:str = "branches"):
        self._base_path = Path(ConfigManager.get_configs().user_data.dir)
        self._base_name = sanitize_filename(base_name)
        if not validate_path(self._base_path, self._base_name):
            raise ValueError(f"Invalid path \"{self._base_name}\" for \"{self._base_path}\"")
        self.sub_managers: WeakValueDictionary[str, SubManager] = WeakValueDictionary()

        self.cache_metadata = cache_metadata
        self.cache_data = cache_data

        self.sub_dir_name = branches_dir_name
    
    @property
    def base_path(self):
        return self._base_path / self._base_name
    
    def _get_sub_manager(self, user_id: str) -> SubManager:
        if user_id not in self.sub_managers:
            self.sub_managers[user_id] = SubManager(
                self.base_path / user_id,
                cache_metadata = self.cache_metadata,
                cache_data = self.cache_data,
                sub_dir_name = self.sub_dir_name,
            )
        
        return self.sub_managers[user_id]
    
    async def _get_branch_id(self, user_id: str) -> str:
        manager = self._get_sub_manager(user_id)
        try:
            metadata = await manager.load_metadata()
        except Exception as e:
            logger.error(
                "Read User Metadata File Error: {error}",
                user_id = user_id,
                error = e
            )
            raise
        
        if isinstance(metadata, dict):
            branch_name = metadata.get(ConfigManager.get_configs().user_data.metadata_fields.branch_field, "default")
            if not isinstance(branch_name, str):
                branch_name = ConfigManager.get_configs().user_data.default_branch_name
                metadata[ConfigManager.get_configs().user_data.metadata_fields.branch_field] = branch_name
                await manager.save_metadata(metadata)
        else:
            branch_name = ConfigManager.get_configs().user_data.default_branch_name
        
        return branch_name
    
    async def load(self, user_id: str, default: Any = None) -> Any:
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        
        try:
            return await manager.load(branch_id, default)
        except Exception as e:
            logger.error(
                "Read User File Error: {error}",
                user_id = user_id,
                error = e
            )
            raise
    
    async def save(self, user_id: str, data: Any) -> None:
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        try:
            await manager.save(branch_id, data)
        except Exception as e:
            logger.error(
                "Write User File Error: {error}",
                user_id = user_id,
                error = e
            )
            raise
    
    async def delete(self, user_id: str) -> None:
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)

        try:
            await manager.delete(branch_id)
        except Exception as e:
            logger.error(
                "Delete User File Error: {error}",
                user_id = user_id,
                error = e
            )
            raise
    
    async def set_default_branch_id(self, user_id: str, branch_id: str) -> None:
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)

        if isinstance(metadata, dict):
            metadata[ConfigManager.get_configs().user_data.metadata_fields.branch_field] = branch_id
        else:
            metadata = {ConfigManager.get_configs().user_data.metadata_fields.branch_field: branch_id}
        
        try:
            await manager.save_metadata(metadata)
        except Exception as e:
            logger.error(f"Write User Metadata File Error: {e}", user_id = user_id)
            raise
    
    async def get_default_branch_id(self, user_id: str) -> str:
        user_id = sanitize_filename(user_id)
        branch_id = await self._get_branch_id(user_id)
        return branch_id

    async def get_all_user_id(self) -> list:
        return [f.name for f in (self.base_path).iterdir() if f.is_dir()]

    async def get_all_branch_id(self, user_id: str) -> list:
        return [f.stem for f in (self.base_path / user_id / self.sub_dir_name).iterdir() if f.is_file()]