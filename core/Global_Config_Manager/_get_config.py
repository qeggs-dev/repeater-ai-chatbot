import os
from ._loader import ConfigManager
from ._base_model import Global_Config

def get_config(config_dir: str | os.PathLike) -> Global_Config:
    loader = ConfigManager(config_dir)
    return loader.load()