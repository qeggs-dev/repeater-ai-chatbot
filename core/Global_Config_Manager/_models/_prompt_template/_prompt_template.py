from pydantic import BaseModel, ConfigDict, Field
from ._bot_info import Bot_Info_Config
from ._time import Time_Config


class Prompt_Template_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    version: str | None = None
    bot_info: Bot_Info_Config = Field(default_factory=Bot_Info_Config)
    time: Time_Config = Field(default_factory=Time_Config)
    default_user_profile: str = "The user has not filled out the field for the time being."