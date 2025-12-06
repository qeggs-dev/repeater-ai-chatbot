from dataclasses import dataclass, field
from ._top_logprob import Top_Logprob

@dataclass
class Logprob:
    """
    Dataclass to store the logprobs data for a given date.
    """
    token: str = ""
    logprob: float = 0.0
    top_logprobs: list[Top_Logprob] = field(default_factory=list)