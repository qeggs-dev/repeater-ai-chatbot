from pydantic import BaseModel, ConfigDict, Field
from ._cache_data import Cache_Data_Config
from ._metadata_fields import MetadataFields

class User_Data_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    dir: str = "./workspace/data/user_data"
    branches_dir_name: str = "branches"
    default_branch_id: str = "main"
    file_size_use_abbreviation: bool = True
    metadata_file_name: str = "metadata.json"
    cache_medadata: bool | Cache_Data_Config = False
    cache_data: bool | Cache_Data_Config = False
    cross_user_data_access: bool = False
    metadata_fields:MetadataFields = Field(default_factory=MetadataFields)