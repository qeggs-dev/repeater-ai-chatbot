import os
from ._loader import ConfigManager
from ._base_model import GlobalConfigs

def get_config(config_dir: str | os.PathLike) -> GlobalConfigs:
    loader = ConfigManager()
    return loader.load(temp_loadpath = config_dir)