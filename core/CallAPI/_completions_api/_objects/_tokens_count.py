from dataclasses import dataclass, asdict
import math

@dataclass
class TokensCount:
    """
    Dataclass to store the token usage data for a given date.
    """
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    prompt_cache_hit_tokens: int = 0
    prompt_cache_miss_tokens: int = 0

    @property
    def prompt_cache_hit_ratio(self) -> float:
        if self.prompt_cache_hit_tokens is not None and self.prompt_cache_miss_tokens is not None:
            if self.prompt_cache_hit_tokens + self.prompt_cache_miss_tokens > 0:
                return self.prompt_cache_hit_tokens / (self.prompt_cache_hit_tokens + self.prompt_cache_miss_tokens)
        return math.nan
    
    @property
    def as_dict(self) -> dict[str, int]:
        return asdict(self)