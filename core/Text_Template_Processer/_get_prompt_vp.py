import random
import numpy as np

from ..Global_Config_Manager import Global_Config
from ..User_Config_Manager import UserConfigs
from ..Assist_Struct import Request_User_Info
from TextProcessors import PromptVP, str_to_bool
from .._info import __version__
from ._value_comparison import value_comparison, ComparisonOperator
from ..ApiInfo import ApiObject

from datetime import datetime, timedelta
from TimeParser import (
    get_timezone_offset,
    get_birthday_countdown,
    date_to_zodiac,
    format_timestamp,
    calculate_age,
)
from uuid import uuid4
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
            model: ApiObject = ApiObject(),
            user_info: Request_User_Info = Request_User_Info(),
            global_config: Global_Config = Global_Config(),
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
        bot_name = global_config.prompt_template.bot_info.name
        bot_birthday_year = global_config.prompt_template.bot_info.birthday.year
        bot_birthday_month = global_config.prompt_template.bot_info.birthday.month
        bot_birthday_day = global_config.prompt_template.bot_info.birthday.day
        timezone = config.timezone or global_config.prompt_template.time.timezone
        now = datetime.now()

        if isinstance(timezone, str):
            time_offset = get_timezone_offset(
                timezone = timezone,
                dt = now
            )
        else:
            time_offset = timedelta(hours=timezone)
        
        prompt_vp = self.get_prompt_vp(
            user_id = user_id,
            birthday_countdown = lambda detailed_mode = False: get_birthday_countdown(
                bot_birthday_month,
                bot_birthday_day,
                name=bot_name,
                precise = str_to_bool(detailed_mode),
            ),
            reprs = lambda *args: "\n".join([repr(arg) for arg in args]),
            version = global_config.prompt_template.version or __version__,
            model_uid = model.uid,
            model_name = model.name,
            model_id = model.id,
            model_type = model.type.value,
            model_group = model.parent,
            botname = bot_name,
            username = user_info.username or "Unknown",
            nickname = user_info.nickname or "Unknown",
            user_age = user_info.age or "Unknown",
            user_gender = user_info.gender or "Unknown",
            user_info = user_info.model_dump(exclude_none=True),
            birthday = f"{bot_birthday_year}-{bot_birthday_month}-{bot_birthday_day}",
            zodiac = lambda **kw: date_to_zodiac(bot_birthday_month, bot_birthday_day),
            time = lambda time_format = "%Y-%m-%d(%A) %H:%M:%S %Z": format_timestamp(now, time_offset, time_format),
            age = lambda **kw: calculate_age(bot_birthday_year, bot_birthday_month, bot_birthday_day, offset_timezone = time_offset),
            random = lambda min, max: random.randint(int(min), int(max)),
            randfloat = lambda min, max: random.uniform(float(min), float(max)),
            randchoice = lambda *args: random.choice(args),
            generate_uuid = lambda **kw: uuid4(),
            copytext = lambda text, number, spacers = "": spacers.join([text] * int(number)),
            text_matrix = lambda text, columns, lines, spacers = " ", line_breaks = "\n": line_breaks.join(spacers.join([text] * int(columns)) for _ in range(int(lines))),
            random_matrix = lambda rows, cols: np.random.rand(int(rows), int(cols)),
            user_profile = lambda: config.user_profile if config.user_profile is not None else global_config.prompt_template.default_user_profile,
            **kwargs
        )

        # if 是 Python 关键字，所以需要单独处理
        prompt_vp.register_variable("if", lambda value_1, compare_operator, value_2: value_comparison(value_1, value_2, ComparisonOperator(compare_operator), True))

        return prompt_vp