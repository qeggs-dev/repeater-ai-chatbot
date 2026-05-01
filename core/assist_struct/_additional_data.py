from pydantic import BaseModel

class AdditionalData(BaseModel):
    image_url: str | list[str] | None = None
    video_url: str | list[str] | None = None
    audio_url: str | list[str] | None = None
    file_url: str | list[str] | None = None

    def __bool__(self) -> bool:
        return any([self.image_url, self.video_url, self.audio_url, self.file_url])