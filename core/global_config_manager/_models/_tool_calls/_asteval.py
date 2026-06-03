from pydantic import BaseModel


class Asteval(BaseModel):
    max_threads: int = 32