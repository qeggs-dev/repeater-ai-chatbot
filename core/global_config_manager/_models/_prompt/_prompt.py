from pydantic import BaseModel, ConfigDict, Field

class PromptConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    base_path: str = "/prompt/presets"
    suffix: str = ".md"
    encoding: str = "utf-8"
    preset_name: str = "official/normal/repeater"
    load_prompt: bool = True
    directive_base_path: str = "/prompt/directives"
    prompt_directives: dict[str, list[str]] = Field(default_factory=dict)
    force_load_directives: dict[str, list[str]] = Field(default_factory=dict)