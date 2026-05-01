from yarl import URL
from ..auxiliary.path import sanitize_filename_with_dir
from ..static_resources_client import StaticResourcesClient

class Styles:
    def __init__(self, static_resources_client: StaticResourcesClient, style_base_path: str | URL):
        self._static_resources_client = static_resources_client
        self._style_base_path = URL(style_base_path)
    
    def get_style_full_url(self, style_name: str) -> URL:
        return self._static_resources_client.base_url.join(self.get_style_url(style_name))
    
    def get_style_url(self, style_name: str) -> URL:
        style_name = sanitize_filename_with_dir(style_name)
        style_file_path: URL = self._style_base_path / f"{style_name}.css"
        return style_file_path