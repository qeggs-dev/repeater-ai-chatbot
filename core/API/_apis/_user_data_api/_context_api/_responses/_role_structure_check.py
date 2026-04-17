from pydantic import BaseModel
from ......context_manager import (
    ContentRole
)

class RoleStructureCheckerResponse(BaseModel):
    message: str = "No role structure error found"
    index: int = -1
    role: ContentRole | None = None
    expected_role: list[ContentRole] | None = None