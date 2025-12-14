from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from .._exceptions import *
from ._content_role import ContentRole
from typing import Any

class ContentUnit(BaseModel):
    """
    上下文单元
    """
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    reasoning_content:str = ""
    content: str = ""
    role: ContentRole = ContentRole.USER
    role_name: str |  None = None
    prefix: bool | None = None
    tool_call_id: str | None = None

    def __len__(self) -> int:
        return len(self.content) + len(self.reasoning_content)
    
    def to_content(self, remove_resoning_prompt: bool = False) -> dict[str, Any]:
        if remove_resoning_prompt:
            return self.model_dump(exclude = {"reasoning_content"})
        return self.model_dump()
    
    def __bool__(self) -> bool:
        return bool(self.content) or bool(self.reasoning_content) or bool(self.tool_call_id)