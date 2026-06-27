from pydantic import BaseModel, ConfigDict, Field

class PreprocessMapConfig(BaseModel):
    before: dict[str, str] = Field(default_factory=dict)
    after: dict[str, str] = Field(default_factory=dict)