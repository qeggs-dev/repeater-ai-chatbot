import os
from ._loader import ConfigManager
from ._base_model import Base_Config

def get_config(config_dir: str | os.PathLike) -> Base_Config:
    loader = ConfigManager(config_dir)
    return loader.load()