from pydantic import BaseModel, Field, ConfigDict
from typing import Any
from ._timestamp_object import TimeStamp
from ._logprob import Logprob

class RequestLog(BaseModel):
    """
    Class to represent a request log object.
    """
    model_config = ConfigDict(
        validate_assignment=True,
    )
    
    id: str = ""
    url: str = ""
    model: str = ""
    user_id: str = ""
    task_id: str = ""
    user_name: str | None = None
    stream: bool = True

    total_chunk: int = 0
    empty_chunk: int = 0

    task_start_time: TimeStamp = Field(default_factory=lambda: TimeStamp(timestamp=0, monotonic=0))
    prepare_start_time: TimeStamp = Field(default_factory=lambda: TimeStamp(timestamp=0, monotonic=0))
    prepare_end_time: TimeStamp = Field(default_factory=lambda: TimeStamp(timestamp=0, monotonic=0))
    request_start_time: TimeStamp = Field(default_factory=lambda: TimeStamp(timestamp=0, monotonic=0))
    request_end_time: TimeStamp = Field(default_factory=lambda: TimeStamp(timestamp=0, monotonic=0))
    stream_processing_start_time: TimeStamp = Field(default_factory=lambda: TimeStamp(timestamp=0, monotonic=0))
    stream_processing_end_time: TimeStamp = Field(default_factory=lambda: TimeStamp(timestamp=0, monotonic=0))
    task_end_time: TimeStamp = Field(default_factory=lambda: TimeStamp(timestamp=0, monotonic=0))
    chunk_generated_times: list[TimeStamp] = Field(default_factory=list)
    translation_chunk_times: list[TimeStamp] = Field(default_factory=list)
    translation_queue_backlog: list[int] = Field(default_factory=list)
    chunk_times: list[TimeStamp] = Field(default_factory=list)
    queue_backlog: list[int] = Field(default_factory=list)
    created_time: int = 0

    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_hit_count: int = 0
    cache_miss_count: int = 0
    logprob: Logprob | list[Logprob] | None = None

    total_context_length: int = 0
    reasoning_content_length: int = 0
    new_content_length: int = 0