from pydantic import BaseModel, Field
from .....Context_Manager import ContentRole
from .....Request_User_Info import Request_User_Info

class ChatRequest(BaseModel):
    message: str = ""
    user_info: Request_User_Info = Field(default_factory=Request_User_Info)
    role: ContentRole = ContentRole.USER
    role_name: str | None = None
    model_uid: str | None = None
    load_prompt: bool | None = None
    save_context: bool | None = None
    save_new_only: bool | None = None
    temporary_prompt: str | None = None
    image_url: str | list[str] | None = None
    reference_context_id: str | None = None
    continue_completion: bool = False
    stream: bool = False