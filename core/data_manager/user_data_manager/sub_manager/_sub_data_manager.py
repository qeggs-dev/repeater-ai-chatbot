# ==== 标准库 ==== #
import os
import asyncio
from typing import Any, Generator
from pathlib import Path

# ==== 第三方库 ==== #
import orjson
import aiofiles

from cachetools import LRUCache
from loguru import logger

# ==== 项目库 ==== #
from ....auxiliary.path import validate_path, sanitize_filename
from ....pools.lock_pool import AsyncLockPool
from .._fname_b64_encoder import fname_b64_encode, fname_b64_decode
from ....global_config_manager import ConfigManager
from ._branch_info import BranchInfo

class SubManager:
    def __init__(
            self,
            base_path: str | os.PathLike,
            sub_dir_name: str,
            cache_metadata:bool = False,
            cache_data:bool = False,
            cache_maxsize:int | float = float("inf"),
        ):
        self.base_path: Path = Path(base_path)
        self.sub_dir_name: str = sanitize_filename(sub_dir_name)
        self._global_lock: asyncio.Lock = asyncio.Lock()
        self._branches_locks: AsyncLockPool = AsyncLockPool()
        
        self._metadata_filename = ConfigManager.get_configs().user_data.metadata_file_name
        
        self.cache_metadata:bool = cache_metadata
        self._metadata_cache: Any = {}

        self.cache_data:bool = cache_data
        self._data_cache_size: int | float = cache_maxsize
        self._data_cache: LRUCache[str, Any] = LRUCache(
            maxsize = self._data_cache_size
        )

    @property
    def _default_base_file(self) -> Path:
        """
        Gets the default file path.
        """
        return self.base_path / self.sub_dir_name
    @property
    def _get_metadata_file_path(self) -> Path:
        """
        Gets the path to the metadata file.
        """
        return self.base_path / self._metadata_filename
    
    def _get_file_path(self, name: str) -> Path:
        """
        Gets the actual file path for the given name.
        
        Args:
            name (str): The name of the file.
        """
        # if not self._default_base_file.exists():
        #     self._default_base_file.mkdir(parents=True, exist_ok=True)
        name = sanitize_filename(name)
        file_name = f"{fname_b64_encode(name)}.json"
        if not validate_path(self._default_base_file, file_name):
            raise ValueError(f"Invalid file name: {file_name}")
        return self._default_base_file / file_name
    
    async def _get_branch_lock(self, branch_id: str) -> asyncio.Lock:
        """
        Gets the lock for the branch, or creates a lock for the branch if none exists

        
        Args:
            branch_id (str): The branch id to get the lock for
        """
        async with self._global_lock:
            lock: asyncio.Lock = await self._branches_locks.get_lock(branch_id)
        return lock
    
    async def load_metadata(self, default: Any | None = None) -> Any:
        """
        Load metadata from file

        Args:
            default (Any, optional): Default value if file does not exist. Defaults to None.

        Returns:
            Metadata (Any): The metadata
        """
        async with self._global_lock:
            try:
                if self.cache_metadata and self._metadata_cache is not None:
                    logger.info("Using cached metadata")
                    return self._metadata_cache
                else:
                    if not self._get_metadata_file_path.exists():
                        logger.info("Metadata file does not exist")
                        return default
                    async with aiofiles.open(self._get_metadata_file_path, "rb") as f:
                        fdata = await f.read()
                        metadata = await asyncio.to_thread(orjson.loads, fdata)
                        if self.cache_metadata:
                            self._metadata_cache = metadata
                        logger.info("Loaded metadata")
                        return metadata
            except FileNotFoundError:
                return default
            except orjson.JSONDecodeError:
                return default
    
    async def save_metadata(self, data: Any):
        """
        Save metadata to file

        Args:
            data (Any): Metadata to save
        """
        async with self._global_lock:
            if not self.base_path.exists():
                self.base_path.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(self._get_metadata_file_path, "wb") as f:
                fdata = await asyncio.to_thread(orjson.dumps, data)
                await f.write(fdata)
            if self.cache_metadata:
                self._metadata_cache = data
            logger.info("Saved metadata")
    
    async def load(self, branch_id: str, default: Any | None = None) -> Any:
        """
        Load data from file

        Args:
            branch_id (str): Branch ID to load
            default (Any | None): Default value if item not found. Defaults to None.
        Returns:
            data (Any): Loaded data
        """
        async with await self._get_branch_lock(branch_id):
            try:
                if self.cache_data and self._data_cache is not None and branch_id in self._data_cache:
                    logger.info("Loading data from cache")
                    return self._data_cache[branch_id]
                else:
                    path = self._get_file_path(branch_id)
                    if not path.exists():
                        logger.info("Data file not found")
                        return default
                    async with aiofiles.open(path, "rb") as f:
                        fdata = await f.read()
                        data = await asyncio.to_thread(orjson.loads, fdata)
                        if self.cache_data:
                            self._data_cache[branch_id] = data
                        logger.info("Loaded data")
                        return data
            except FileNotFoundError:
                return default
            except orjson.JSONDecodeError:
                return default
    
    async def save(self, branch_id: str, data: Any) -> None:
        """
        Save data to a file.

        Args:
            branch_id (str): The name of the branch to save.
            data (Any): The data to save.
        """
        async with await self._get_branch_lock(branch_id):
            path = self._get_file_path(branch_id)
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(self._get_file_path(branch_id), "wb") as f:
                await f.write(await asyncio.to_thread(orjson.dumps, data))
            if self.cache_data:
                self._data_cache[branch_id] = data
            logger.info("Saved data")
    
    async def delete(self, branch_id: str) -> None:
        """
        Delete a file from the cache.

        Args:
            branch_id (str): The item of the file to delete.
        """
        async with await self._get_branch_lock(branch_id):
            try:
                loop = asyncio.get_event_loop()
                def remove_data():
                    os.remove(self._get_file_path(branch_id))
                    if self.cache_data:
                        del self._data_cache[branch_id]
                await loop.run_in_executor(None, remove_data)
                logger.info("Deleted data")
            except FileNotFoundError:
                pass
    
    async def bind(self, src_branch_id: str, dst_branch_id: str) -> None:
        """
        Bind a branch to another branch.

        Use hard links to bind a branch to another branch.

        Args:
            src_branch_id (str): The branch to bind from.
            dst_branch_id (str): The branch to bind to.
        """
        async with await self._get_branch_lock(src_branch_id):
            src_path = self._get_file_path(src_branch_id)
            dst_path = self._get_file_path(dst_branch_id)
            if not src_path.exists():
                raise FileNotFoundError(f"{src_path} does not exist.")
            if dst_path.exists():
                raise FileExistsError(f"{dst_path} already exists.")
            dst_path.hardlink_to(src_path)
            logger.info(
                "Hardlinked {src_path} to {dst_path}",
                src_path = src_path,
                dst_path = dst_path
            )
    
    def exists(self, branch_id: str) -> bool:
        """
        Check if a branch exists.

        Args:
            branch_id (str): The branch to check.

        Returns:
            branch_exists (bool): True if the branch exists, False otherwise.
        """
        return self._get_file_path(branch_id).exists()
    
    async def info(self, branch_id: str) -> BranchInfo:
        """
        Get the info of a branch.

        Args:
            branch_id (str): The branch to get the info of.

        Returns:
            branch_info (BranchInfo): The info of the branch.
        """
        async with await self._get_branch_lock(branch_id):
            path = self._get_file_path(branch_id)
            if not path.exists():
                return BranchInfo(
                    branch_id = branch_id,
                    size = 0,
                    modified_time = 0.0,
                    file_exists = False,
                )
            
            info = path.stat()
            return BranchInfo(
                branch_id = branch_id,
                size = info.st_size,
                modified_time = info.st_mtime,
                file_exists = True,
            )