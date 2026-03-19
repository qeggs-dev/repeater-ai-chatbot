from pydantic import BaseModel, ConfigDict
from ....Markdown_Render.html_render import BrowserType

class HTML_To_Image_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    output_dir: str = "./workspace/temp/render"
    max_pages_per_browser: int = 5
    max_browsers: int = 2
    base_url: str | None = None
    browser_type: BrowserType = BrowserType.AUTO
    headless: bool = True
    route_blacklist_file: str | None = None
    output_suffix: str = ".png"
    executable_path: str | None = None
    width: int = 1200
    height: int = 600
    quality: int = 90