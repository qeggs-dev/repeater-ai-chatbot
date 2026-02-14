from pydantic import BaseModel, ConfigDict, Field
from ._sandbox import SandboxConfig
from ._time import Time_Config


class TextTemplateConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    version: str | None = None
    sandbox: SandboxConfig = Field(default_factory=SandboxConfig)
    time: Time_Config = Field(default_factory=Time_Config)
    default_user_profile: str = "The user has not filled out the field for the time being."