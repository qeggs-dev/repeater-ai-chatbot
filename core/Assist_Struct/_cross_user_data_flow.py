from pydantic import BaseModel, Field

class DataFlowField(BaseModel):
    """
    Cross Data Flow.

    Where the mentor gets its resources.
    """
    from_user_id_load: str | None = None
    to_user_id_save: str | None = None


class CrossUserDataFlow(BaseModel):
    """
    Cross User Data Flow.

    Where the mentor gets its resources.
    """
    context: DataFlowField = Field(default_factory=DataFlowField)
    prompt: DataFlowField = Field(default_factory=DataFlowField)
    config: DataFlowField = Field(default_factory=DataFlowField)

    