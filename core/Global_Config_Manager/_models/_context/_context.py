from pydantic import BaseModel, ConfigDict

class Context_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    context_shrink_limit: int | None = None
    save_context: bool = True
    save_text_only: bool = False