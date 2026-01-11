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
        metadata = await manager.load_metadata()
        
        if isinstance(metadata, dict):
            branch_name = metadata.get(ConfigManager.get_configs().user_data.metadata_fields.branch_field, "default")
            if not isinstance(branch_name, str):
                branch_name = ConfigManager.get_configs().user_data.default_branch_name
                metadata[ConfigManager.get_configs().user_data.metadata_fields.branch_field] = branch_name
                logger.warning(
                    "Branch name is not a string, using default branch name."
                )
                await manager.save_metadata(metadata)
        else:
            branch_name = ConfigManager.get_configs().user_data.default_branch_name
        
        return branch_name
    
    async def load(self, user_id: str, default: Any | None = None) -> Any:
        """
        Load a user's data from file system.

        Args:
            user_id (str): The user's ID.
            default (Any | None, optional): The default value to return if the user's data is not found. Defaults to None.

        Returns:
            Any: The user's data.
        """
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        
        return await manager.load(branch_id, default)
    
    async def save(self, user_id: str, data: Any) -> None:
        """
        Save a user's data to file system.

        Args:
            user_id (str): The user's ID.
            data (Any): The user's data.
        """
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)

        await manager.save(branch_id, data)
    
    async def delete(self, user_id: str) -> None:
        """
        Delete a user's data from file system.

        Args:
            user_id (str): The user's ID.
        """
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)

        await manager.delete(branch_id)
    
    async def clone(self, user_id: str, new_branch_id: str, default: Any | None = None) -> None:
        """
        Clone a user's data to a new branch.

        Args:
            user_id (str): The user's ID.
            new_branch_id (str): The new branch ID.
            default (Any | None): The default data to use if the branch does not exist.
        """
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)

        loaded_data = await manager.load(branch_id, default)
        await manager.save(new_branch_id, loaded_data)
    
    async def clone_from(self, user_id: str, source_branch_id: str, default: Any | None = None) -> None:
        """
        Clone data from another branch.

        Args:
            user_id (str): The user ID.
            source_branch_id (str): The source branch ID.
            default (Any | None): The default data to use if the branch does not exist.
        """
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)

        loaded_data = await manager.load(source_branch_id, default)
        await manager.save(branch_id, loaded_data)
    
    async def binding(self, user_id: str, new_branch_id: str) -> None:
        """
        Binding now active branch to an another branch.

        Args:
            user_id (str): User ID.
            new_branch_id (str): New branch ID.
        """
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        manager.binding(branch_id, new_branch_id)
    
    async def binding_from(self, user_id: str, source_branch_id: str) -> None:
        """
        Binding an another branch to now active branch.

        Warning:
            This method will override now active branch.

        Args:
            user_id (str): User ID.
            source_branch_id (str): The source branch ID.
        """
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        manager.delete(branch_id)
        manager.binding(source_branch_id, branch_id)

    
    async def set_default_branch_id(self, user_id: str, branch_id: str) -> None:
        """
        Set the default branch ID for a user.

        Args:
            user_id (str): The user ID.
            branch_id (str): The branch ID.
        """
        user_id = sanitize_filename(user_id)
        manager = self._get_sub_manager(user_id)

        if isinstance(metadata, dict):
            metadata[ConfigManager.get_configs().user_data.metadata_fields.branch_field] = branch_id
        else:
            metadata = {ConfigManager.get_configs().user_data.metadata_fields.branch_field: branch_id}
        
        await manager.save_metadata(metadata)
    
    async def get_default_branch_id(self, user_id: str) -> str:
        """
        Get the default branch ID from a user.

        Args:
            user_id (str): The user ID.
        
        Returns:
            str: The default branch ID.
        """
        user_id = sanitize_filename(user_id)
        branch_id = await self._get_branch_id(user_id)
        return branch_id

    async def get_all_user_id(self) -> list:
        """
        Get all user IDs.

        Returns:
            list: A list of all user IDs.
        """
        return [f.name for f in (self.base_path).iterdir() if f.is_dir()]

    async def get_all_branch_id(self, user_id: str) -> list:
        """
        Get all branch IDs for a given user ID.

        Args:
            user_id (str): The user ID.
        
        Returns:
            list: A list of branch IDs.
        """
        return [f.stem for f in (self.base_path / user_id / self.sub_dir_name).iterdir() if f.is_file()]