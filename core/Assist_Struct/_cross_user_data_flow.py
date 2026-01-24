from pydantic import BaseModel, Field
from typing import TypeVar, Generic

T = TypeVar('T')

class DataFlowField(BaseModel, Generic[T]):
    """
    Cross Data Flow.

    Where the mentor gets its resources.
    """
    load_from_user_id: T = None
    save_to_user_id: T = None

    def fill_undefined(self, user_id: T):
        """
        Fill undefined fields.
        """
        if self.load_from_user_id is None:
            self.load_from_user_id = user_id
        if self.save_to_user_id is None:
            self.save_to_user_id = user_id
    
    def is_all_defined(self) -> bool:
        """
        Check if all fields are defined.
        """
        return (
            self.load_from_user_id is not None and
            self.save_to_user_id is not None
        )


class CrossUserDataFlow(BaseModel, Generic[T]):
    """
    Cross User Data Flow.

    Where the mentor gets its resources.
    """
    context: DataFlowField[T] = Field(default_factory=DataFlowField)
    prompt: DataFlowField[T] = Field(default_factory=DataFlowField)
    config: DataFlowField[T] = Field(default_factory=DataFlowField)

    def fill_undefined(self, user_id: T):
        self.context.fill_undefined(user_id)
        self.prompt.fill_undefined(user_id)
        self.config.fill_undefined(user_id)
    
    def is_all_defined(self) -> bool:
        return (
            self.context.is_all_defined() and
            self.prompt.is_all_defined() and
            self.config.is_all_defined()
        )