from pydantic import BaseModel, ConfigDict
from .auxiliary.background import Background
from .auxiliary.moderation import Moderation
from .auxiliary.output_format import OutputFormat
from .auxiliary.quality import Quality
from .auxiliary.response_format import ImageResponseFormat
from .auxiliary.size import ImageSize
from .auxiliary.style import ImageStyle

class ImagesRequest(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True
    )
    
    prompt: str
    background: Background | None = None
    model: str | None = None
    moderation: Moderation | None = None
    n: int | None = None
    output_compression: int | None = None
    output_format: OutputFormat | None = None
    partial_images: int | None = None
    quality: Quality | None = None
    response_format: ImageResponseFormat | None = None
    size: ImageSize | str | None = None
    stream: bool | None = False
    style: ImageStyle | None = None
    user: str | None = None
    timeout: int | float | None = None