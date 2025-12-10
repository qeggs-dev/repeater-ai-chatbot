from pydantic import BaseModel

class RewriteContext(BaseModel):
    index: int
    content: str | None = None
    reasoning_content: str | None = None