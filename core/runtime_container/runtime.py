from __future__ import annotations

# ==== 标准库 ==== #
from pathlib import Path

# ==== 第三方库 ==== #
from loguru import logger
from environs import Env

# ==== 自定义库 ==== #
from ..auxiliary.time import print_init_runtime
from ..data_manager import (
    ContextManager,
    PromptManager
)
from ..user_config_manager import (
    ConfigManager as UserConfigManager
)
from ..pools.resource_pool import ResourcePool
from ..text_buffer import ContentBuffer
from ..auxiliary.regex_checker import RegexChecker
from ..global_config_manager import ConfigManager
from ..clients.model_info import (
    ModelsClient
)
from ..clients.nexus_client import NexusClient
from ..clients.html_render_client import HTMLRenderClient
from ..licenses_loader import LicenseLoader
from ..clients.static_resources_client import StaticResourcesClient
from ..request_log import (
    RequestLogManager
)
from ..status_map import StatusMap
from ..pools.awaitable_pool import TaskPool
from ..pools.openai_pool import OpenAIPool
from ..auxiliary.http import get_ssl_context

class RepeaterRuntime:
    _env = Env()

    def __init__(self):
        all_obj = dir(self)
        for obj in all_obj:
            if obj.startswith("init_") and hasattr(self, obj):
                func = getattr(self, obj)
                func()

    @print_init_runtime("Data Manager")
    def init_data_manager(self):
        # 初始化用户数据管理器
        self.context_manager = ContextManager()
        self.prompt_manager = PromptManager()
        self.user_config_manager: UserConfigManager = UserConfigManager()

    @print_init_runtime("Models Manager")
    def init_models_manager(self):
        # 初始化 Model 管理器
        self.model_info_client = ModelsClient(
            ConfigManager.get_configs().model_api.base_url,
            self._env.str(
                ConfigManager.get_configs().model_api.api_key_env_name
            ),
            ConfigManager.get_configs().model_api.timeout,
            verify = get_ssl_context()
        )

    @print_init_runtime("Static Resources Client")
    def init_static_resources_client(self):
        # 初始化静态资源客户端
        self.static_resources_client = StaticResourcesClient(
            ConfigManager.get_configs().static_resources_server.base_url,
            ConfigManager.get_configs().static_resources_server.timeout,
            verify = get_ssl_context()
        )

    @print_init_runtime("Content Buffers Pool")
    def init_content_buffers_pool(self):
        # 初始化内容缓冲池
        self.content_buffers_pool: ResourcePool[ContentBuffer] = ResourcePool()

    @print_init_runtime("Call Log Manager")
    def init_call_log_manager(self):
        # 初始化调用日志管理器
        self.request_log = RequestLogManager(
            ConfigManager.get_configs().request_log.dir,
            auto_save = ConfigManager.get_configs().request_log.auto_save,
        )

    @print_init_runtime("Blacklist")
    def init_blacklist(self):
        # 黑名单
        self.blacklist: RegexChecker = RegexChecker()
        blacklist_file_path = Path(ConfigManager.get_configs().blacklist.file_path)
        try:
            with open(blacklist_file_path, "r", encoding="utf-8") as f:
                self.blacklist.load_strstream(f)
        except ValueError:
            logger.error("Invalid blacklist file")
        except FileNotFoundError:
            logger.error(f"Blacklist file not found: {blacklist_file_path}")
        self.blacklist_match_timeout: int | None = ConfigManager.get_configs().blacklist.match_timeout

    @print_init_runtime("Task Status Map")
    def init_task_status_map(self):
        # Task 状态表
        self.task_status_map: StatusMap[str, str] = StatusMap()

    @print_init_runtime("Chat Task Pool")
    def init_chat_task_pool(self):
        # 初始化任务池
        self.chat_task_pool: TaskPool = TaskPool()

    @print_init_runtime("Openai Pool")
    def init_openai_pool(self):
        # 初始化客户端池
        self.openai_pool: OpenAIPool = OpenAIPool()

    @print_init_runtime("HTML Render Client")
    def init_html_render_client(self):
        render_config = ConfigManager.get_configs().render
        self.html_render_client = HTMLRenderClient(
            base_url = render_config.to_image.base_url,
            timeout = render_config.to_image.timeout,
            verify = get_ssl_context()
        )
    
    @print_init_runtime("Nexus Client")
    def init_nexus_client(self):
        nexus_config = ConfigManager.get_configs().nexus
        self.nexus_client: NexusClient = NexusClient(
            base_url = nexus_config.base_url,
            request_timeout = nexus_config.api_timeout,
            verify = get_ssl_context()
        )
    
    @print_init_runtime("License Loader")
    def init_licenses_data(self):
        self.licenses = LicenseLoader(ConfigManager.get_configs().licenses)
        self.licenses.scan_licenses()