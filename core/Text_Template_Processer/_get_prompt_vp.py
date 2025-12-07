from ..Global_Config_Manager import ConfigManager
from ..User_Config_Manager import UserConfigs
from ..Request_User_Info import Request_User_Info
from TextProcessors import PromptVP, str_to_bool
from .. import __version__
from ._value_comparison import value_comparison

from datetime import datetime, timedelta
from TimeParser import (
    get_timezone_offset,
    get_birthday_countdown,
    date_to_zodiac,
    format_timestamp,
    calculate_age,
)
import random
from uuid import uuid4
import numpy as np
from typing import Any

class PromptVP_Loader:
    def __init__(self, **kwargs):
        self._variable = kwargs

    # def __init__(self, config: UserConfigManager, prompt: PromptManager, context: ContextManager):
    #     self.config = config
    #     self.prompt = prompt
    #     self.context = context

    def get_prompt_vp(
            self,
            **kwargs: Any
        ) -> PromptVP:
        """Get prompt variable processor"""
        prompt_vp = PromptVP()

        prompt_vp.bulk_register_variable(**self._variable)
        prompt_vp.bulk_register_variable(**kwargs)
    
        return prompt_vp

    def get_prompt_vp_ex(
            self,
            user_id: str,
            model_uid: str = "",
            user_info: Request_User_Info = Request_User_Info(),
            config: UserConfigs = UserConfigs(),
            **kwargs
        ) -> PromptVP:
        """
        获取指定用户的PromptVP实例

        :param user_id: 用户ID
        :param model_uid: 模型UID
        :param user_info: 用户信息
        :param config: 用户配置
        :return: PromptVP实例
        """
        bot_name = ConfigManager.get_configs().prompt_template.bot_info.name
        bot_birthday_year = ConfigManager.get_configs().prompt_template.bot_info.birthday.year
        bot_birthday_month = ConfigManager.get_configs().prompt_template.bot_info.birthday.month
        bot_birthday_day = ConfigManager.get_configs().prompt_template.bot_info.birthday.day
        timezone = config.timezone or ConfigManager.get_configs().prompt_template.time.timezone
        now = datetime.now()

        if isinstance(timezone, str):
            time_offset = get_timezone_offset(
                timezone = timezone,
                dt = now
            )
        else:
            time_offset = timedelta(hours=timezone)

        
        return self.get_prompt_vp(
            user_id = user_id,
            birthday_countdown = lambda detailed_mode = False: get_birthday_countdown(
                bot_birthday_month,
                bot_birthday_day,
                name=bot_name,
                detailed_mode = str_to_bool(detailed_mode),
            ),
            reprs = lambda *args: "\n".join([repr(arg) for arg in args]),
            version = ConfigManager.get_configs().prompt_template.version or __version__,
            model_uid = model_uid if model_uid else config.model_uid,
            botname = bot_name,
            username = user_info.username or "None",
            nickname = user_info.nickname or "None",
            user_age = user_info.age or "None",
            user_gender = user_info.gender or "None",
            user_info = user_info.as_dict,
            birthday = f"{bot_birthday_year}-{bot_birthday_month}-{bot_birthday_day}",
            zodiac = lambda **kw: date_to_zodiac(bot_birthday_month, bot_birthday_day),
            time = lambda time_format = "%Y-%m-%d %H:%M:%S %Z": format_timestamp(now, time_offset, time_format),
            age = lambda **kw: calculate_age(bot_birthday_year, bot_birthday_month, bot_birthday_day, offset_timezone = time_offset),
            random = lambda min, max: random.randint(int(min), int(max)),
            randfloat = lambda min, max: random.uniform(float(min), float(max)),
            randchoice = lambda *args: random.choice(args),
            generate_uuid = lambda **kw: uuid4(),
            copytext = lambda text, number, spacers = "": spacers.join([text] * int(number)),
            text_matrix = lambda text, columns, lines, spacers = " ", line_breaks = "\n": line_breaks.join(spacers.join([text] * int(columns)) for _ in range(int(lines))),
            random_matrix = lambda rows, cols: np.random.rand(int(rows), int(cols)),
            **kwargs
        )