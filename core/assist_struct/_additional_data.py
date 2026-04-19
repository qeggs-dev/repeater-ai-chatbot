from pydantic import BaseModel

class AdditionalData(BaseModel):
    image_url: str | list[str] | None = None
    video_url: str | list[str] | None = None
    audio_url: str | list[str] | None = None
    file_url: str | list[str] | None = None