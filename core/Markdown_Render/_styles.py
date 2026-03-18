# _styles.py
# Markdown 渲染样式预设 - 纯色主题

import os
import aiofiles
from yarl import URL
from PathProcessors import sanitize_filename_with_dir
from ..Static_Resources_Client import StaticResourcesClient
from loguru import logger

class Styles:
    def __init__(self, static_resources_client: StaticResourcesClient, style_base_path: str | URL):
        self._static_resources_client = static_resources_client
        self._style_base_path = URL(style_base_path)
    
    async def get_style(self, style_name: str, use_base: bool = True, encoding: str = "utf-8") -> str:
        style_name = sanitize_filename_with_dir(style_name)
        style_file_path: URL = self._style_base_path / f"{style_name}.css"
        
        try:
            return await self._static_resources_client.get_text(style_file_path, text_encoding = encoding)
        except (FileNotFoundError, ValueError):
            logger.error(f"Style file not found: {style_file_path}")
            raise ValueError(f"Style file not found: {style_file_path}")