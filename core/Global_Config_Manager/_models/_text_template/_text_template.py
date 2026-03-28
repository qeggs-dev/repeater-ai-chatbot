from pydantic import BaseModel, ConfigDict, Field
from ._sandbox import SandboxConfig
from ._time import Time_Config

class Enable_Template_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    user_input_template: bool = False
    assistant_template: bool = False
    request_statistics_template: bool = False
    api_template: bool = False

class TextTemplateConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    version: str | None = None
    sandbox: SandboxConfig = Field(default_factory=SandboxConfig)
    time: Time_Config = Field(default_factory=Time_Config)
    default_user_profile: str = ""
    enable: Enable_Template_Config = Field(default_factory=Enable_Template_Config)