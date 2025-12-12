from pydantic import BaseModel

class InjectContext(BaseModel):
    user_content: str
    assistant_content: str