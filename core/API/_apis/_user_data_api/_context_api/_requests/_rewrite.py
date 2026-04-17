from pydantic import BaseModel
from ......context_manager import ContentUnit

class RewriteContext(BaseModel):
    index: int
    content: ContentUnit