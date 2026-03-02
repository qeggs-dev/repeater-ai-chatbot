from pydantic import BaseModel
from typing import Any

class EnvironmentModel(BaseModel):
    context: Any
    prompt: Any
    config: dict