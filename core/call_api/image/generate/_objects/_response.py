from pydantic import BaseModel, ConfigDict
from .auxiliary.image import Image
from .auxiliary.background import Background
from .auxiliary.output_format import OutputFormat
from .auxiliary.quality import Quality
from .auxiliary.size import ImageSize
from .auxiliary.token_usage import ImageTokenUsage

class ImagesResponse(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True
    )

    created: int = 0
    background: Background | None = None
    data: list[Image] | None = None
    output_format: OutputFormat | None = None
    quality: Quality | None = None
    size: ImageSize | str | None = None
    usage: ImageTokenUsage | None = None