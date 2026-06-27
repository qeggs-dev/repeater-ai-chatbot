from pydantic import BaseModel, ConfigDict

class RequestLogConfig(BaseModel):
    dir: str = "./workspace/request_log"
    auto_save: bool = True
    debonce_save_wait_time: float = 600.0
    cache_keep_time: float = 600.0
    max_cache_size: int = 1000
    full_memory_cache: bool = False