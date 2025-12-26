from pydantic import BaseModel, ConfigDict, Field
from .....Markdown_Render import HTML_Render

class RenderTime(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True
    )

    preprocess: int | None = None
    markdown_to_html: int | None = None
    render: int | None = None


class Render_Response(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True
    )

    image_url: str | None = None,
    file_uuid: str | None = None,
    style: str | None = None,
    status: HTML_Render.RenderStatus | None = None,
    browser_used: str | None = None,
    url_expiry_time: float | None = None,
    error: str | None = None,
    text: str | None = None,
    image_render_time_ms: float | None = None,
    created: int | None = None,
    created_ms: int | None = None,
    details_time: RenderTime | None = None