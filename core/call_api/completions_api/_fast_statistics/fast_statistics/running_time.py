from pydantic import BaseModel
from ..format import format_timedelta

class RunningTime(BaseModel):
    request_info: int = 0
    response: int = 0
    chunk_count: int = 0
    time: int = 0
    chunk_statistics: int = 0
    token_count: int = 0
    content: int = 0

    def format(self):
        members = self.model_dump()
        formated: list[str] = []
        for key, value in members.items():
            formated.append(f"{key}: {format_timedelta(value)}")
        return "\n".join(formated)