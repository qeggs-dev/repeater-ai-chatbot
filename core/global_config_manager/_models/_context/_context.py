from pydantic import BaseModel, ConfigDict

class ContextConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    context_shrink_limit: int | None = None
    save_context: bool = True
    save_text_only: bool = False
    save_new_only: bool = False
    tool_calling_remove_reasoning: bool = False
    remove_reasoning_prompt: bool = True
    make_multimodal_message: bool = True

    max_log_length_for_non_text_content: int | None = 25