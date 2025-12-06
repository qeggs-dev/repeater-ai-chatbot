from dataclasses import dataclass

@dataclass
class Top_Logprob:
    token: str = ""
    logprob: float = 0.0