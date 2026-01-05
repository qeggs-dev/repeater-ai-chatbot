import os
import yaml
import orjson
import asyncio
import aiofiles
import threading
from pathlib import Path

from pydantic import validate_call
from ._pydantic_models import ApiInfoConfig, ApiGroup
from ..Global_Config_Manager import ConfigManager
from ._model_type import ModelType
from ._api_obj import ApiObject
from ._exceptions import *

class ApiInfo:
    def __init__(self, case_sensitive: bool = False):
        if not isinstance(case_sensitive, bool):
            raise TypeError("case_sensitive must be a boolean")
        self._api_objs: dict[ModelType, dict[str, list[ApiObject]]] = {}
        self._case_sensitive: bool = case_sensitive
        self._api_info_async_lock = asyncio.Lock()
        self._api_info_lock = threading.Lock()

        # Initialize the indexs
        for model_type in ModelType:
            self._api_objs[model_type] = {}


    def _create_api_group(self, api_data: list[dict]) -> ApiGroup:
        """Create an ApiGroup instance from raw data."""
        return ApiGroup(api = api_data)

    def _parse_api_groups(self, raw_api_groups: list[dict]) -> None:
        """Parse raw API groups data and populate indexes."""
        default_timeout = ConfigManager.get_configs().model.default_timeout
        
        api_groups: ApiGroup = self._create_api_group(raw_api_groups)
        self._api_groups: ApiGroup = api_groups

        for group in api_groups.api:
            for model in group.models:

                if model.timeout is not None:
                    model_timeout: float = group.timeout
                elif group.timeout is not None:
                    model_timeout: float = group.timeout
                else:
                    model_timeout: float = default_timeout
                
                api_obj = ApiObject(
                    name = model.name,
                    uid = model.uid,
                    id = model.id,
                    api_key_env = group.api_key_env,
                    parent = group.name,
                    url = model.url or group.url,
                    type = model.type,
                    timeout = model_timeout,
                )
                if api_obj.uid not in self._api_objs:
                    self._api_objs[model.type][api_obj.uid] = [api_obj]
                else:
                    self._api_objs[model.type][api_obj.uid].append(api_obj)

    @validate_call
    def load(self, path: str | os.PathLike) -> None:
        """Load and parse API groups from a JSON/YAML file."""
        path: Path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File \"{path}\" does not exist")
        with self._api_info_lock:
            if path.suffix.lower() == ".json":
                try:
                    with open(path, "rb") as f:
                        fdata = f.read()
                        raw_api_groups: list[dict] = orjson.loads(fdata)
                        self._parse_api_groups(raw_api_groups)
                except orjson.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON format: {e}")
                except OSError as e:
                    raise IOError(f"Failed to read file: {e}")
            elif path.suffix.lower() == ".yaml" or path.suffix.lower() == ".yml":
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        fdata = f.read()
                        raw_api_groups: list[dict] = yaml.safe_load(fdata)
                        self._parse_api_groups(raw_api_groups)
                except yaml.YAMLError as e:
                    raise ValueError(f"Invalid YAML format: {e}")
                except OSError as e:
                    raise IOError(f"Failed to read file: {e}")
            else:
                raise ValueError(f"Invalid file format: {path.suffix}")

    @validate_call
    async def load_async(self, path: str | os.PathLike) -> None:
        """Load and parse API groups from a JSON/YAML file."""
        path: Path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File \"{path}\" does not exist")
        async with self._api_info_async_lock:
            if path.suffix.lower() == ".json":
                try:
                    async with aiofiles.open(path, "rb") as f:
                        fdata = await f.read()
                        raw_api_groups: list[dict] = orjson.loads(fdata)
                        await self._parse_api_groups(raw_api_groups)
                except orjson.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON format: {e}")
                except OSError as e:
                    raise IOError(f"Failed to read file: {e}")
            elif path.suffix.lower() == ".yaml" or path.suffix.lower() == ".yml":
                try:
                    async with aiofiles.open(path, "r", encoding="utf-8") as f:
                        fdata = await f.read()
                        raw_api_groups: list[dict] = yaml.safe_load(fdata)
                        await self._parse_api_groups(raw_api_groups)
                except yaml.YAMLError as e:
                    raise ValueError(f"Invalid YAML format: {e}")
                except OSError as e:
                    raise IOError(f"Failed to read file: {e}")
            else:
                raise ValueError(f"Invalid file format: {path.suffix}")

    @validate_call
    def find(self, model_type: ModelType, model_uid: str, default: list[ApiObject] | None = None) -> list[ApiObject]:
        """Find API groups by model uid."""
        if self._case_sensitive:
            key = model_uid
        else:
            key = model_uid.lower()

        index_list = self._api_objs[model_type].get(key, default)
        if index_list is None:
            return []
        
        return index_list.copy()
    
    @validate_call
    def uid_list(self, model_type: ModelType) -> list[str]:
        """Get a list of all model uids."""
        if not isinstance(model_type, ModelType):
            raise TypeError("model_type must be an instance of ModelType")
        
        return list(self._api_objs[model_type].keys())
    
    @property
    def empty_api_object(self) -> ApiObject:
        return ApiObject()