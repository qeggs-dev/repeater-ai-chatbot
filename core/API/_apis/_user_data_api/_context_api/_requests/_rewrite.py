from pydantic import BaseModel
from ......Context_Manager import ContentUnit

class RewriteContext(BaseModel):
    index: int
    content: ContentUnit