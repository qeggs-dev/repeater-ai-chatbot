from pydantic import BaseModel, Field, ConfigDict

class StreamOptions(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    include_obfuscation: bool | None = None
    include_usage: bool | None = None