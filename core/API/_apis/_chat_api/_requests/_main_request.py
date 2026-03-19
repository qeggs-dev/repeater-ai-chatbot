from pydantic import BaseModel, Field
from .....Context_Manager import ContentRole, ContentUnit
from .....Assist_Struct import Request_User_Info, CrossUserDataRouting, AdditionalData
from typing import Any

class ChatRequest(BaseModel):
    message: str | None = ""
    history_messages: list[ContentUnit] | None = None
    user_info: Request_User_Info = Field(default_factory=Request_User_Info)
    role: ContentRole = ContentRole.USER
    assistant_role: ContentRole = ContentRole.ASSISTANT
    history_msg_role_map: dict[ContentRole, ContentRole | None] | None = None
    role_name: str | None = None
    model_uid: str | None = None
    thinking: bool | None = None
    load_prompt: bool | None = None
    save_context: bool | None = None
    save_new_only: bool | None = None
    temporary_prompt: str | None = None
    extra_template_fields: dict[str, Any] | None = None
    additional_data: AdditionalData | None = None
    cross_user_data_routing: CrossUserDataRouting[str | None] | None = None
    stream: bool = False