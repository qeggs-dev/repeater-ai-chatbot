from typing import Any
from pydantic import BaseModel, Field
from ._finish_reason import FinishReason
from ._tokens_count import TokensCount
from ._tool_calls import ToolCall
from ....request_log import Logprob

class Delta(BaseModel):
    """
    Dataclass to store the delta data for a given date.
    """
    id: str = ""
    reasoning_content: str = ""
    content: str = ""
    tool_calls: list[ToolCall] | None = None
    token_usage: TokensCount = Field(default_factory=TokensCount)
    finish_reason: FinishReason | str | None = None
    created: int = 0
    model: str = ""
    system_fingerprint: str | None = None
    logprobs: list[Logprob] = Field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        """
        Check if the delta data is empty.
        """
        return not (self.reasoning_content or self.content or self.tool_calls or self.token_usage)