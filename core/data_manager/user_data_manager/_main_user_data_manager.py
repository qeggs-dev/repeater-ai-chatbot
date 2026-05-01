# ==== 标准库 ==== #
import base64

from typing import TypeVar, Generic, Callable
from pathlib import Path

# ==== 第三方库 ==== #
from loguru import logger

# ==== 自定义库 ==== #
from .sub_manager import SubManager, BranchInfo
from ...auxiliary.path import validate_path, sanitize_filename
from ._fname_b64_encoder import fname_b64_encode, fname_b64_decode
from ...global_config_manager import ConfigManager

T = TypeVar("T")

class UserDataManager(Generic[T]):
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
            self.base_path / fname_b64_encode(user_id),
            cache_metadata = self._cache_metadata,
            cache_data = self._cache_data,
            sub_dir_name = self._sub_dir_name,
        )
        return manager
    
    def _get_default_value(self, default_value: T | None) -> T:
        if default_value is not None:
            return default_value
        
        elif self._default_factory is None:
            return None
        
        elif callable(self._default_factory):
            return self._default_factory()
        
        else:
            raise ValueError("Get default value failed.")
    
    async def load(self, *, user_id: str, branch_id: str | None = None, default: T | None = None) -> T:
        """
        Load a user's data from file system.

        Args:
            user_id (str): The user's ID.
            branch_id (str): The branch ID.
            default (Any | None, optional): The default value to return if the user's data is not found. Defaults to None.

        Returns:
            Any: The user's data.
        """
        manager = self._get_sub_manager(user_id)
        default_value = self._get_default_value(default)
        if branch_id is None:
            branch_id = await self.get_active_branch_id(user_id)

        logger.info(
            "Loading [Branch:{base_name}/{encoded_user_id}/{src_branch_id}]",
            user_id = user_id,
            base_name = self._base_name,
            encoded_user_id = fname_b64_encode(user_id),
            src_branch_id = fname_b64_encode(branch_id)
        )
        
        return await manager.load(branch_id, default_value)
    
    async def save(self, *, user_id: str, branch_id: str | None = None, data: T) -> None:
        """
        Save a user's data to file system.

        Args:
            user_id (str): The user's ID.
            branch_id (str): The branch ID.
            data (Any): The user's data.
        """
        manager = self._get_sub_manager(user_id)
        if branch_id is None:
            branch_id = await self.get_active_branch_id(user_id)

        logger.info(
            "Saving [Branch:{base_name}/{encoded_user_id}/{dst_branch_id}]",
            user_id = user_id,
            base_name = self._base_name,
            encoded_user_id = fname_b64_encode(user_id),
            dst_branch_id = fname_b64_encode(branch_id)
        )

        await manager.save(branch_id, data)
    
    async def delete(self, *, user_id: str, branch_id: str | None = None) -> None:
        """
        Delete a user's data from file system.

        Args:
            user_id (str): The user's ID.
            branch_id (str): The branch ID.
        """
        manager = self._get_sub_manager(user_id)
        if branch_id is None:
            branch_id = await self.get_active_branch_id(user_id)

        logger.info(
            "Deleting [Branch:{base_name}/{encoded_user_id}/{dst_branch_id}]",
            user_id = user_id,
            base_name = self._base_name,
            encoded_user_id = fname_b64_encode(user_id),
            dst_branch_id = fname_b64_encode(branch_id)
        )

        await manager.delete(branch_id)
    
    async def clone(self, *, user_id: str, branch_id: str | None = None, dst_branch_id: str, default: T | None = None) -> None:
        """
        Clone a user's data to a new branch.

        Args:
            user_id (str): The user's ID.
            branch_id (str): The source branch ID.
            dst_branch_id (str): The ID of the destination branch.
            default (Any | None): The default data to use if the branch does not exist.
        """
        manager = self._get_sub_manager(user_id)
        default_value = self._get_default_value(default)
        if branch_id is None:
            branch_id = await self.get_active_branch_id(user_id)

        logger.info(
            "Cloning [Branch:{base_name}/{encoded_user_id}/{src_branch_id}] to [Branch:{base_name}/{encoded_user_id}/{dst_branch_id}]",
            user_id = user_id,
            base_name = self._base_name,
            encoded_user_id = fname_b64_encode(user_id),
            src_branch_id = fname_b64_encode(branch_id),
            dst_branch_id = fname_b64_encode(dst_branch_id)
        )

        loaded_data = await manager.load(branch_id, default_value)
        await manager.save(dst_branch_id, loaded_data)
    
    async def bind(self, *, user_id: str, branch_id: str | None = None, dst_branch_id: str, default: T | None = None) -> None:
        """
        Bind now active branch to an another branch.

        Args:
            user_id (str): User ID.
            branch_id (str): Source branch ID.
            dst_branch_id (str): Destination branch ID.
        """
        manager = self._get_sub_manager(user_id)
        default_value = self._get_default_value(default)
        if branch_id is None:
            branch_id = await self.get_active_branch_id(user_id)

        logger.info(
            "Binding [Branch:{base_name}/{encoded_user_id}/{src_branch_id}] to [Branch:{base_name}/{encoded_user_id}/{dst_branch_id}]",
            user_id = user_id,
            base_name = self._base_name,
            encoded_user_id = fname_b64_encode(user_id),
            src_branch_id = fname_b64_encode(branch_id),
            dst_branch_id = fname_b64_encode(dst_branch_id)
        )

        if not manager.exists(branch_id):
            logger.warning(
                "[Branch:{base_name}/{encoded_user_id}/{src_branch_id}] does not exist, creating...",
                user_id = user_id,
                base_name = self._base_name,
                encoded_user_id = fname_b64_encode(user_id),
                src_branch_id = fname_b64_encode(branch_id)
            )
            await manager.save(branch_id, default_value)
        if manager.exists(dst_branch_id):
            logger.warning(
                "[Branch:{base_name}/{encoded_user_id}/{dst_branch_id}] already exists, deleting...",
                user_id = user_id,
                base_name = self._base_name,
                encoded_user_id = fname_b64_encode(user_id),
                dst_branch_id = fname_b64_encode(dst_branch_id)
            )
            await manager.delete(dst_branch_id)
        await manager.bind(branch_id, dst_branch_id)
    
    async def set_active_branch_id(self, user_id: str, branch_id: str) -> None:
        """
        Set the active branch id for a user.

        Args:
            user_id (str): The user id.
            branch_id (str): The branch id.
        """
        manager = self._get_sub_manager(user_id)
        metadata = await manager.load_metadata()

        if isinstance(metadata, dict):
            metadata[ConfigManager.get_configs().user_data.metadata_fields.branch_field] = branch_id
        else:
            metadata = {ConfigManager.get_configs().user_data.metadata_fields.branch_field: branch_id}
        
        logger.info(
            "Set Active Branch to [Branch:{base_name}/{encoded_user_id}/{dst_branch_id}]",
            user_id = user_id,
            base_name = self._base_name,
            encoded_user_id = fname_b64_encode(user_id),
            dst_branch_id = fname_b64_encode(branch_id),
        )
        
        await manager.save_metadata(metadata)
    
    async def get_active_branch_id(self, user_id: str) -> str:
        """
        Get the active branch id from a user.

        Args:
            user_id (str): The user id.
        
        Returns:
            str: The default branch id.
        """
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
    
    async def info(self, user_id: str) -> BranchInfo:
        """
        Get the user's information.

        Args:
            user_id (str): The user ID.
        
        Returns:
            dict: The user's information.
        """
        manager = self._get_sub_manager(user_id)
        branch_id = await self.get_active_branch_id(user_id)

        return await manager.info(branch_id)

    async def get_all_user_id(self) -> list:
        """
        Get all user IDs.

        Returns:
            list: A list of all user IDs.
        """
        return [fname_b64_decode(f.name) for f in (self.base_path).iterdir() if f.is_dir()]

    async def get_all_branch_id(self, user_id: str) -> list[str]:
        """
        Get all branch IDs for a given user ID.

        Args:
            user_id (str): The user ID.
        
        Returns:
            list: A list of branch IDs.
        """
        if not (self.base_path / fname_b64_encode(user_id)).exists():
            return []
        branch_ids: list[str] = []
        base_path = self.base_path / fname_b64_encode(user_id) / self._sub_dir_name
        for branch_id in base_path.iterdir():
            if branch_id.exists() and branch_id.is_file():
                branch_ids.append(fname_b64_decode(branch_id.stem))
        return branch_ids