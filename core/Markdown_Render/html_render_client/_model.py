from pydantic import BaseModel, ConfigDict, Field
from ._render_status import RenderStatus

class RenderTime(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True
    )

    preprocess: int | None = None
    render: int | None = None


class Render_Response(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True
    )

    image_url: str
    file_uuid: str
    status: RenderStatus
    browser_used: str
    url_expiry_time: float
    error: str | None = None
    content: str = ""
    image_render_time_ms: float = 0.0
    created: int = 0
    created_ms: int = 0
    details_time: RenderTime = Field(default_factory=RenderTime)