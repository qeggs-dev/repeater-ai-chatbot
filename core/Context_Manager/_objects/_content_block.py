from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Union
from enum import StrEnum

class ContentBlockType(StrEnum):
    TEXT = "text"
    IMAGE_URL = "image_url"
    INPUT_AUDIO = "input_audio"
    FILE = "file"


class TextBlock(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )
    type: Literal[ContentBlockType.TEXT] = ContentBlockType.TEXT
    text: str = ""

class ImageUrlBlock(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    url: str = ""

class ImageBlock(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    type: Literal[ContentBlockType.IMAGE_URL] = ContentBlockType.IMAGE_URL
    image_url: ImageUrlBlock = Field(default_factory=ImageUrlBlock)

class AudioDataBlock(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    data: str = ""

class AudioBlock(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    type: Literal[ContentBlockType.INPUT_AUDIO] = ContentBlockType.INPUT_AUDIO
    input_audio: AudioDataBlock = Field(default_factory=AudioDataBlock)

class FileDataBlock(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    file_data: str = ""
    file_id: str = ""
    filename: str = ""

class FileBlock(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    type: Literal[ContentBlockType.FILE] = ContentBlockType.FILE
    file: FileDataBlock = Field(default_factory=FileDataBlock)

ContentBlock = Union[
    TextBlock,
    ImageBlock,
    AudioBlock,
    FileBlock
]