from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from ._data_types import DataTypes
from ._metadata_fields import MetadataFields

class UserDataConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    dir: str = "./workspace/data/user_data"
    branches_dir_name: str = "branches"
    default_branch_id: str = "main"
    b64_encode_path: bool = True
    snapshot_directory_name: str = "snapshots"
    metadata_file_name: str = "metadata.json"
    cache_medadata: bool | DataTypes[bool] = False
    cache_data: bool | DataTypes[bool] = False
    user_data_cache_maxsize: int | Literal["infinite", "inf"] = 8
    max_sub_manager_cache_size: int | Literal["infinite", "inf"] = 1024
    cross_user_data_access: bool = False
    metadata_fields:MetadataFields = Field(default_factory=MetadataFields)

    def get_user_data_cache_maxsize(self) -> int | float:
        if self.user_data_cache_maxsize in ["infinite", "inf"]:
            return float("inf")
        return self.user_data_cache_maxsize
    
    def get_max_sub_manager_cache_size(self) -> int | float:
        if self.max_sub_manager_cache_size in ["infinite", "inf"]:
            return float("inf")
        return self.max_sub_manager_cache_size