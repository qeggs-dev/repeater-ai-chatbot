from pydantic import BaseModel, Field
from typing import Literal

class SearchParameters(BaseModel):
    q: str
    scope:Literal["webpage", "document", "scholar", "image", "video", "podcast"]
    size: int
    includeSummary: bool
    includeRawContent: bool
    conciseSnippet: bool
    format: str = "chat_completions"

class Content(BaseModel):
    title: str
    link: str
    score: str
    snippet: str
    position: int
    authors: list[str]
    date: str

class Response(BaseModel):
    credits: int
    searchParameters: SearchParameters

    webpages: list[Content] = Field(default_factory=list)
    documents: list[Content] = Field(default_factory=list)
    scholars: list[Content] = Field(default_factory=list)
    images: list[Content] = Field(default_factory=list)
    videos: list[Content] = Field(default_factory=list)
    podcasts: list[Content] = Field(default_factory=list)