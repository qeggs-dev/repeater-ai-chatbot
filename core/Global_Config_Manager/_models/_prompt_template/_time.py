from pydantic import BaseModel, ConfigDict, Field

class Time_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    time_offset: float = Field(0.0, ge=-12.0, le=14.0)