from pydantic import BaseModel, ConfigDict

class PromptConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    dir: str = "./configs/prompt/presets"
    suffix: str = ".md"
    encoding: str = "utf-8"
    preset_name: str = "default"
    load_prompt: bool = True