from pydantic import BaseModel, ConfigDict, Field
from .....Markdown_Render import HTML_Render

class RenderTime(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True
    )

    preprocess: int = 0
    markdown_to_html: int = 0
    render: int = 0


class Render_Response(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True
    )

    image_url: str = "",
    file_uuid: str = "",
    style: str = "",
    status: HTML_Render.RenderStatus = HTML_Render.RenderStatus.SUCCESS,
    browser_used: str = "",
    url_expiry_time: float = 0.0,
    error: str = "",
    text: str = "",
    image_render_time_ms: float = 0.0,
    created: int = 0,
    created_ms: int = 0,
    details_time: RenderTime = Field(default_factory=RenderTime)