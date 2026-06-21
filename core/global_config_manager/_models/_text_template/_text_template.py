from pydantic import BaseModel, ConfigDict, Field
from ._sandbox import SandboxConfig
from ._time import TimeConfig

class EnableTemplateConfig(BaseModel):
    user_input_template: bool = False
    assistant_template: bool = False
    request_statistics_template: bool = False
    api_template: bool = False

class TextTemplateConfig(BaseModel):
    version: str | None = None
    sandbox: SandboxConfig = Field(default_factory=SandboxConfig)
    time: TimeConfig = Field(default_factory=TimeConfig)
    default_user_profile: str = ""
    request_statistics_template: str = "Total Tokens: {{request_log.total_tokens}} | Input: {{request_log.prompt_tokens}} | Output: {{request_log.completion_tokens}}"
    enable: EnableTemplateConfig = Field(default_factory=EnableTemplateConfig)