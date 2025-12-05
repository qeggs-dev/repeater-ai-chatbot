from pydantic import BaseModel, ConfigDict

class Context_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    context_shrink_limit: int | None = None