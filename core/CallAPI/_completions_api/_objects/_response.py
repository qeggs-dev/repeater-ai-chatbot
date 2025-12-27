from pydantic import BaseModel, ConfigDict, Field
from ....Context_Manager import ContextObject
from ....Request_Log import RequestLog, TimeStamp
from ._tokens_count import TokensCount
from ._finish_reason import FinishReason
from ._logprob import Logprob


class Response(BaseModel):
    """
    This class is used to store the response data
    """
    model_config = ConfigDict(
        validate_assignment=True
    )

    id: str = ""
    context: ContextObject = Field(default_factory=ContextObject)
    created: int = 0
    model: str = ""
    token_usage: TokensCount | None = None
    stream: bool = False

    stream_processing_start_time_ns:TimeStamp = Field(default_factory=TimeStamp)
    stream_processing_end_time_ns:TimeStamp = Field(default_factory=TimeStamp)
    chunk_times: list[TimeStamp] = Field(default_factory=list)
    finish_reason: FinishReason = FinishReason.STOP
    system_fingerprint: str = ""
    logprobs: list[Logprob] | None = None
    calling_log: RequestLog = Field(default_factory=RequestLog)

    @property
    def finish_reason_cause(self) -> str:
        match self.finish_reason:
            case FinishReason.STOP:
                reason = "Reached STOP list or natural stopping point."
            case FinishReason.LENGTH:
                reason = "Exceeded maximum output length limit."
            case FinishReason.CONTENT_FILTER:
                reason = "Content triggered filtering policy."
            case FinishReason.TOOL_CALLS:
                reason = "Output contains tool calls."
            case FinishReason.INSUFFICIENT_SYSTEM_RESOURCE:
                reason = "Insufficient system resource to complete the request."
            case _:
                reason = "Unknown"
        return reason
