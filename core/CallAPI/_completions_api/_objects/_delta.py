from typing import Any
from dataclasses import dataclass, asdict, field
from ._finish_reason import FinishReason
from ._tokens_count import TokensCount
from ._logprob import Logprob

@dataclass
class Delta:
    """
    Dataclass to store the delta data for a given date.
    """
    id: str = ""
    reasoning_content: str = ""
    content: str = ""
    function_id: str = ""
    function_type: str = ""
    function_name: str = ""
    function_arguments: str = ""
    token_usage: TokensCount = field(default_factory=TokensCount)
    finish_reason: FinishReason | None = None
    created: int = 0
    model: str = ""
    system_fingerprint: str = ""
    logprobs: list[Logprob] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        """
        Check if the delta data is empty.
        """
        return not (self.reasoning_content or self.content or self.function_name or self.function_arguments or self.token_usage)
    
    @property
    def as_dict(self) -> dict[str, Any]:
        """
        Convert the delta data to a dictionary.
        """
        return asdict(self)