from pydantic import BaseModel, Field, ConfigDict
from typing import TypeVar, Generic
from ..User_Config_Manager import (
    ConfigManager as UserConfigManager
)
from ..Global_Config_Manager import (
    ConfigManager as GlobalConfigManager
)
from loguru import logger

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
            logger.warning(
                "load_from_user_id is not defined, using {user_id}",
                user_id = user_id
            )
            self.load_from_user_id = user_id
        if self.save_to_user_id is None:
            logger.warning(
                "save_to_user_id is not defined, using {user_id}",
                user_id = user_id
            )
            self.save_to_user_id = user_id
    
    def is_all_defined(self) -> bool:
        """
        Check if all fields are defined.
        """
        return (
            self.load_from_user_id is not None and
            self.save_to_user_id is not None
        )
    async def remove_not_allowed_user(self, user_id: str, user_config_manager: UserConfigManager):
        """
        Removes a target user that is not allowed access.
        """
        if self.load_from_user_id != user_id:
            user_config = await user_config_manager.load(self.load_from_user_id)
            if user_config.cross_user_data_access is None:
                if not GlobalConfigManager.get_configs().user_data.cross_user_data_access:
                    logger.warning(
                        "Global config does not allow cross user data access.",
                        user_id = user_id
                    )
                    self.load_from_user_id = user_id
            else:
                if not user_config.cross_user_data_access:
                    logger.warning(
                        "User {dst_user_id} is not allowed to access cross user data.",
                        user_id = user_id,
                        dst_user_id = self.load_from_user_id
                    )
                    self.load_from_user_id = user_id
        if self.save_to_user_id != user_id:
            user_config = await user_config_manager.load(self.save_to_user_id)
            if user_config.cross_user_data_access is None:
                if not GlobalConfigManager.get_configs().user_data.cross_user_data_access:
                    logger.warning(
                        "Global config does not allow cross user data access.",
                        user_id = user_id
                    )
                    self.save_to_user_id = user_id
            else:
                if not user_config.cross_user_data_access:
                    logger.warning(
                        "User {dst_user_id} is not allowed to access cross user data.",
                        user_id = user_id,
                        dst_user_id = self.save_to_user_id
                    )
                    self.save_to_user_id = user_id


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
    
    async def removal_not_allowed_user(self, user_id: T, user_config_manager: UserConfigManager):
        """
        Removes a target user that is not allowed access.
        """
        await self.context.remove_not_allowed_user(user_id, user_config_manager)
        await self.prompt.remove_not_allowed_user(user_id, user_config_manager)
        await self.config.remove_not_allowed_user(user_id, user_config_manager)