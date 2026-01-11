# ==== 标准库 ==== #
from typing import TypeVar, Generic, Callable
from pathlib import Path
from weakref import WeakValueDictionary

# ==== 第三方库 ==== #
from loguru import logger

# ==== 自定义库 ==== #
from .SubManager import SubManager, BranchInfo
from PathProcessors import validate_path, sanitize_filename
from ...Global_Config_Manager import ConfigManager

T = TypeVar("T")

class MainManager(Generic[T]):
    def __init__(
            self,
            base_name: str,
            cache_metadata:bool = False,
            cache_data:bool = False,
            branches_dir_name:str = "branches",
            default_factory: Callable[[], T] | None = None
        ):
        self._base_path = Path(ConfigManager.get_configs().user_data.dir)
        self._base_name = sanitize_filename(base_name)
        if not validate_path(self._base_path, self._base_name):
            raise ValueError(f"Invalid path \"{self._base_name}\" for \"{self._base_path}\"")

        self._cache_metadata = cache_metadata
        self._cache_data = cache_data

        self._sub_dir_name = branches_dir_name

        if default_factory is None:
            self._default_factory = lambda: None
        elif callable(default_factory):
            self._default_factory = default_factory
        else:
            raise ValueError("default_factory must be callable or None")
    
    @property
    def default_factory(self) -> Callable[[], T]:
        return self._default_factory
    
    @property
    def base_path(self):
        return self._base_path / self._base_name
    
    def _get_sub_manager(self, user_id: str) -> SubManager:
        manager = SubManager(
            self.base_path / user_id,
            cache_metadata = self._cache_metadata,
            cache_data = self._cache_data,
            sub_dir_name = self._sub_dir_name,
        )
        return manager
    
    async def _get_branch_id(self, user_id: str) -> str:
        manager = self._get_sub_manager(user_id)
        metadata = await manager.load_metadata()
        
        default_branch_id = ConfigManager.get_configs().user_data.default_branch_id
        if isinstance(metadata, dict):
            branch_name = metadata.get(ConfigManager.get_configs().user_data.metadata_fields.branch_field, default_branch_id)
            if not isinstance(branch_name, str):
                branch_name = default_branch_id
                metadata[ConfigManager.get_configs().user_data.metadata_fields.branch_field] = branch_name
                logger.warning(
                    "Branch name is not a string, using default branch name."
                )
                await manager.save_metadata(metadata)
        else:
            branch_name = default_branch_id
        
        return branch_name
    
    def _get_default_value(self, default_value: T | None) -> T:
        if default_value is not None:
            return default_value
        
        elif self._default_factory is None:
            return None
        
        elif callable(self._default_factory):
            return self._default_factory()
        
        else:
            raise ValueError("Get default value failed.")
    
    async def load(self, user_id: str, default: T | None = None) -> T:
        """
        Load a user's data from file system.

        Args:
            user_id (str): The user's ID.
            default (Any | None, optional): The default value to return if the user's data is not found. Defaults to None.

        Returns:
            Any: The user's data.
        """
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        default_value = self._get_default_value(default)
        
        return await manager.load(branch_id, default_value)
    
    async def save(self, user_id: str, data: T) -> None:
        """
        Save a user's data to file system.

        Args:
            user_id (str): The user's ID.
            data (Any): The user's data.
        """
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)

        await manager.save(branch_id, data)
    
    async def delete(self, user_id: str) -> None:
        """
        Delete a user's data from file system.

        Args:
            user_id (str): The user's ID.
        """
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)

        await manager.delete(branch_id)
    
    async def clone(self, user_id: str, new_branch_id: str, default: T | None = None) -> None:
        """
        Clone a user's data to a new branch.

        Args:
            user_id (str): The user's ID.
            new_branch_id (str): The new branch ID.
            default (Any | None): The default data to use if the branch does not exist.
        """
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        default_value = self._get_default_value(default)

        loaded_data = await manager.load(branch_id, default_value)
        await manager.save(new_branch_id, loaded_data)
    
    async def clone_from(self, user_id: str, source_branch_id: str, default: T | None = None) -> None:
        """
        Clone data from another branch.

        Args:
            user_id (str): The user ID.
            source_branch_id (str): The source branch ID.
            default (Any | None): The default data to use if the branch does not exist.
        """
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        default_value = self._get_default_value(default)

        loaded_data = await manager.load(source_branch_id, default_value)
        await manager.save(branch_id, loaded_data)
    
    async def binding(self, user_id: str, new_branch_id: str, default: T | None = None) -> None:
        """
        Binding now active branch to an another branch.

        Args:
            user_id (str): User ID.
            new_branch_id (str): New branch ID.
        """
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        default_value = self._get_default_value(default)
        if not manager.exists(branch_id):
            await manager.save(branch_id, default_value)
        await manager.binding(branch_id, new_branch_id)
    
    async def binding_from(self, user_id: str, source_branch_id: str, default: T | None = None) -> None:
        """
        Binding an another branch to now active branch.

        Warning:
            This method will override now active branch.

        Args:
            user_id (str): User ID.
            source_branch_id (str): The source branch ID.
        """
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)
        default_value = self._get_default_value(default)
        if not manager.exists(branch_id):
            await manager.save(source_branch_id, default_value)
        await manager.delete(branch_id)
        await manager.binding(source_branch_id, branch_id)

    
    async def set_default_branch_id(self, user_id: str, branch_id: str) -> None:
        """
        Set the default branch ID for a user.

        Args:
            user_id (str): The user ID.
            branch_id (str): The branch ID.
        """
        manager = self._get_sub_manager(user_id)

        if isinstance(metadata, dict):
            metadata[ConfigManager.get_configs().user_data.metadata_fields.branch_field] = branch_id
        else:
            metadata = {ConfigManager.get_configs().user_data.metadata_fields.branch_field: branch_id}
        
        await manager.save_metadata(metadata)
    
    async def info(self, user_id: str) -> BranchInfo:
        """
        Get the user's information.

        Args:
            user_id (str): The user ID.
        
        Returns:
            dict: The user's information.
        """
        manager = self._get_sub_manager(user_id)
        branch_id = await self._get_branch_id(user_id)

        return await manager.info(branch_id)
    
    async def get_default_branch_id(self, user_id: str) -> str:
        """
        Get the default branch ID from a user.

        Args:
            user_id (str): The user ID.
        
        Returns:
            str: The default branch ID.
        """
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
        return [f.stem for f in (self.base_path / user_id / self._sub_dir_name).iterdir() if f.is_file()]