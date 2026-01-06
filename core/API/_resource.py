# ==== 标准库 ==== #
from __future__ import annotations
from typing import ClassVar

# ==== 第三方库 ==== #
from fastapi import FastAPI

# ==== 自定义库 ==== #
from .._core import Core
from AdminApikeyManager import AdminKeyManager
from ._lifespan import lifespan
from ..Global_Config_Manager import ConfigManager
from ..Markdown_Render import HTML_Render

class Resource():
    app: ClassVar[FastAPI | None] = None
    core: ClassVar[Core | None] = None
    admin_key_manager: ClassVar[AdminKeyManager | None] = None
    browser_pool_manager: ClassVar[HTML_Render.BrowserPoolManager | None] = None
    _instance: ClassVar[Resource | None] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def inited(cls):
        if cls.app is None:
            return False
        if cls.core is None:
            return False
        if cls.admin_key_manager is None:
            return False
        if cls.browser_pool_manager is None:
            return False
        return True

    @classmethod
    def init_all(cls):
        cls.init_app()
        cls.init_admin_key_manager()
        cls.init_browser_pool_manager()
    
    @classmethod
    def init_core(cls):
        cls.core = Core()
    
    @classmethod
    def init_app(cls):
        cls.app = FastAPI(
            title="RepeaterChatBackend",
            lifespan = lifespan
        )

    @classmethod
    def init_admin_key_manager(cls):
        # 生成或读取API Key
        cls.admin_key_manager = AdminKeyManager()

    @classmethod
    def init_browser_pool_manager(cls):
        # 渲染配置
        render_config = ConfigManager.get_configs().render
        cls.browser_pool_manager = HTML_Render.BrowserPoolManager(
            max_pages_per_browser = render_config.to_image.max_pages_per_browser,
            max_browsers = render_config.to_image.max_browsers,
            default_browser = render_config.to_image.browser_type,
            headless = render_config.to_image.headless,
            browser_args = HTML_Render.BrowserArgs(
                executable_path = render_config.to_image.executable_path
            )
        )

