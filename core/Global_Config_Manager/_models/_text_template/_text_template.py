from pydantic import BaseModel, ConfigDict, Field
from ._sandbox import SandboxConfig
from ._time import Time_Config


class TextTemplateConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    version: str | None = None
    sandbox: SandboxConfig = Field(default_factory=SandboxConfig)
    time: Time_Config = Field(default_factory=Time_Config)
    default_user_profile: str = ""
    enable_user_input_template: bool = False
    enable_assistant_template: bool = False