from pydantic import BaseModel, ConfigDict

class PromptConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    base_path: str = "/prompt/presets"
    suffix: str = ".md"
    encoding: str = "utf-8"
    preset_name: str = "official/normal/repeater"
    load_prompt: bool = True