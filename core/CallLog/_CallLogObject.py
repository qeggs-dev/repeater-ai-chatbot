from dataclasses import dataclass, field, asdict
from typing import Any
from ._TimeStamp_Obj import TimeStamp

@dataclass
class CallLogObject:
    """
    Class to represent a call log object.
    """
    id: str = ""
    url: str = ""
    model: str = ""
    user_id: str = ""
    user_name: str = ""
    stream: bool = True

    total_chunk: TimeStamp = 0
    empty_chunk: TimeStamp = 0

    task_start_time: TimeStamp = 0
    task_end_time: TimeStamp = 0
    request_start_time: TimeStamp = 0
    request_end_time: TimeStamp = 0
    stream_processing_start_time: TimeStamp = 0
    stream_processing_end_time: TimeStamp = 0
    call_prepare_start_time: TimeStamp = 0
    call_prepare_end_time: TimeStamp = 0
    chunk_times: list[TimeStamp] = field(default_factory=list)
    created_time: TimeStamp = 0

    total_tokens: TimeStamp = 0
    prompt_tokens: TimeStamp = 0
    completion_tokens: TimeStamp = 0
    cache_hit_count: TimeStamp = 0
    cache_miss_count: TimeStamp = 0

    total_context_length: TimeStamp = 0
    reasoning_content_length: TimeStamp = 0
    new_content_length: TimeStamp = 0

    @property
    def as_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict[str: Any]):
        return cls(**data)
    
    def update(self, data: dict[str: Any]):
        for key, value in data.items():
            setattr(self, key, value)
    
@dataclass
class CallAPILogObject:
    """
    Class to represent a call API log object.
    """
    source: str = ""
    start_time: TimeStamp = 0
    end_time: TimeStamp = 0
    user_id: str = ""

    @property
    def as_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict[str: Any]):
        return cls(**data)
    
    def update(self, data: dict[str: Any]):
        for key, value in data.items():
            setattr(self, key, value)