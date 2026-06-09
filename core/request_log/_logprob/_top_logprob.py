from pydantic import BaseModel, ConfigDict

class TopLogprob(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True
    )

    token: str = ""
    logprob: float = 0.0