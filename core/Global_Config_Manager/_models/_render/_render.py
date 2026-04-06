from pydantic import BaseModel, ConfigDict, Field
from ._markdown_to_html import MarkdownToHTMLConfig
from ._html_to_image import HTMLToImageConfig

class RenderConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_image_timeout: float = 60.0

    markdown: MarkdownToHTMLConfig = Field(default_factory=MarkdownToHTMLConfig)
    to_image: HTMLToImageConfig = Field(default_factory=HTMLToImageConfig)