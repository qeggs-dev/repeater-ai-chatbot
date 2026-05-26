from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic

T = TypeVar("T")

class DataTypes(BaseModel, Generic[T]):
    model_config = ConfigDict(case_sensitive=False)

    context: T | None = None
    prompt: T | None = None
    config: T | None = None