from pydantic import BaseModel
from ......context import ContentUnit

class RewriteContext(BaseModel):
    index: int
    content: ContentUnit