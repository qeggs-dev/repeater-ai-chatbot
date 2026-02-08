from pydantic import BaseModel

class RenderRequest(BaseModel):
    text: str
    style: str | None = None
    image_expiry_time: float | None = None
    css: str | None = None
    html_template: str | None = None
    width: int | None = None
    height: int | None = None
    direct_output: bool | None = None
    no_escape: bool = False
    no_pre_labels: bool = False
    quality: int | None = None