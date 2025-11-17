# region imports
# ==== 标准库 ==== #
from pathlib import Path

# ==== 第三方库 ==== #
from environs import Env
env = Env()
from fastapi import FastAPI

# ==== 自定义库 ==== #
from ConfigManager import ConfigLoader
# 一定要提前加载，否则其他模块会无法获取配置内容
configs = ConfigLoader(
    config_file_path = env.path("CONFIG_FILE_PATH", "./configs/project_config.json")
)
import core
from AdminApikeyManager import AdminKeyManager
from PathProcessors import validate_path
# endregion

# region Global Objects
app = FastAPI(title="RepeaterChatBackend")
chat = core.Core()

# 生成或读取API Key
admin_api_key = AdminKeyManager()