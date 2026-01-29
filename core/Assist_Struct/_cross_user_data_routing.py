from pydantic import BaseModel, Field, ConfigDict
from typing import TypeVar, Generic

T = TypeVar('T')

class DataRoutingField(BaseModel, Generic[T]):
    """
    Cross Data Routing Field.

    Where the mentor gets its resources.
    """
    model_config = ConfigDict(
        validate_assignment=True,
    )

    load_from_user_id: T = None
    save_to_user_id: T = None

    def fill_missing(self, user_id: T):
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


class CrossUserDataRouting(BaseModel, Generic[T]):
    """
    Cross User Data Routing.

    Where the mentor gets its resources.
    """
    model_config = ConfigDict(
        validate_assignment=True,
    )

    context: DataRoutingField[T] = Field(default_factory=DataRoutingField)
    prompt: DataRoutingField[T] = Field(default_factory=DataRoutingField)
    config: DataRoutingField[T] = Field(default_factory=DataRoutingField)

    def fill_missing(self, user_id: T):
        self.context.fill_missing(user_id)
        self.prompt.fill_missing(user_id)
        self.config.fill_missing(user_id)
    
    def is_all_defined(self) -> bool:
        return (
            self.context.is_all_defined() and
            self.prompt.is_all_defined() and
            self.config.is_all_defined()
        )