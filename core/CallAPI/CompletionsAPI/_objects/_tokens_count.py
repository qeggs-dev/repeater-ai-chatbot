from pydantic import BaseModel, ConfigDict
import math

class TokensCount(BaseModel):
    """
    Dataclass to store the token usage data for a given date.
    """
    model_config = ConfigDict(
        validate_assignment = True
    )

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    prompt_cache_hit_tokens: int = 0
    prompt_cache_miss_tokens: int = 0

    def cache_hit_ratio(self) -> float:
        if self.prompt_cache_hit_tokens is not None and self.prompt_cache_miss_tokens is not None:
            if self.prompt_cache_hit_tokens + self.prompt_cache_miss_tokens > 0:
                return self.prompt_cache_hit_tokens / (self.prompt_cache_hit_tokens + self.prompt_cache_miss_tokens)
        return math.nan