from pydantic import BaseModel, ConfigDict
from ..CallAPI import CompletionsAPI
from ..Context_Manager import ContentBlock

class Response(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        exclude_none=True,
    )

    reasoning_content: str | None = None
    content: str | None = None
    user_raw_input: str | None = None
    user_input: str | list[ContentBlock] | None = None
    model_group: str | None = None
    model_name: str | None = None
    model_type: str | None = None
    model_uid: str | None = None
    create_time: int | None = None
    id: str | None = None
    finish_reason_cause: str | None = None
    finish_reason_code: CompletionsAPI.FinishReason | None = None
    status: int = 200