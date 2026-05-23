from datetime import datetime
from pydantic import BaseModel, Field

class Index(BaseModel):
    create_time: datetime = Field(default_factory=datetime.now)
    start_file: str = ""
    end_file: str = ""
    status_pointer: int = 0