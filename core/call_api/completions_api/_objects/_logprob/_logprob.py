from pydantic import BaseModel, Field, ConfigDict
from ._top_logprob import TopLogprob

class Logprob(BaseModel):
    """
    Dataclass to store the logprobs data for a given date.
    """
    model_config = ConfigDict(
        validate_assignment = True
    )

    token: str = ""
    logprob: float = 0.0
    top_logprobs: list[TopLogprob] = Field(default_factory=list)