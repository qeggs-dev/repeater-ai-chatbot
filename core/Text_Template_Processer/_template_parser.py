import json
import random
import numpy as np

from ..Global_Config_Manager import Global_Config
from ..User_Config_Manager import UserConfigs
from ..Assist_Struct import Request_User_Info
from .._info import __version__
from ..Model_API import ModelAPI
from jinja2 import Template
from TextProcessors import (
    escape_string
)
from loguru import logger
from datetime import datetime, timedelta
from TimeParser import (
    get_timezone_offset,
    calculation_date_countdown,
    format_time_duration,
    date_to_zodiac,
    format_timestamp,
    calculate_age,
    calculate_precise_age
)
from uuid import uuid4
from typing import Any

class TemplateParser:
    def __init__(
            self,
            model: ModelAPI = ModelAPI(),
            user_info: Request_User_Info = Request_User_Info(),
            global_config: Global_Config = Global_Config(),
            config: UserConfigs = UserConfigs(),
        ):
        self._model = model
        self._user_info = user_info
        self._global_config = global_config
        self._config = config

    def render(
            self,
            text: str,
            /,
            **kwargs: Any
        ) -> str:
        template: Template = Template(text)
        return template.render(
            **kwargs,
        )

    @staticmethod
    def _date_countdown(
            birthday_month: int,
            birthday_day: int ,
            date_name: str,
            precise: bool = False
        ) -> str:
        def time_format(td: timedelta, now: datetime):
            if precise:
                return f"{format_time_duration(td.total_seconds(), use_abbreviation=True)} to {date_name}."
            else:
                return f"{td.days} days to {date_name}."
        
        return calculation_date_countdown(
            target_month = int(birthday_month),
            target_day = int(birthday_day),
            time_format_func = time_format
        )

    def render_ex(
            self,
            text: str,
            user_id: str,
            **kwargs
        ) -> str:
        """
        渲染文本

        :param text: 待渲染的文本
        :param user_id: 用户ID
        :param model_uid: 模型UID
        :param user_info: 用户信息
        :param config: 用户配置
        :return: PromptVP实例
        """
        bot_name = self._global_config.prompt_template.bot_info.name
        bot_birthday_year = self._global_config.prompt_template.bot_info.birthday.year
        bot_birthday_month = self._global_config.prompt_template.bot_info.birthday.month
        bot_birthday_day = self._global_config.prompt_template.bot_info.birthday.day
        timezone = self._config.timezone
        if timezone is None:
            timezone = self._global_config.prompt_template.time.timezone
        
        now = datetime.now()

        def _birthday_countdown(
                birthday_month: int | None = None,
                birthday_day: int | None = None,
                name: str | None = None,
                precise: bool = False
            ) -> str:
            if birthday_month is None:
                birthday_month = bot_birthday_month
            if birthday_day is None:
                birthday_day = bot_birthday_day
            if name is None:
                name = bot_name
            
            def time_format(td: timedelta, now: datetime):
                if precise:
                    return f"And to {name}'s birthday: {format_time_duration(td.total_seconds(), use_abbreviation=True)}"
                else:
                    return f"And to {name}'s birthday: {td.days} days left"
            
            return calculation_date_countdown(
                target_month = int(birthday_month),
                target_day = int(birthday_day),
                time_format_func = time_format,
                is_today_format_func = lambda now: f"Happy birthday to {name}!"
            )

        if isinstance(timezone, str):
            time_offset = get_timezone_offset(
                timezone = timezone,
                dt = now
            )
        else:
            time_offset = timedelta(hours=timezone)
        
        return self.render(
            text,
            user_id = user_id,
            birthday_countdown = _birthday_countdown,
            date_countdown = self._date_countdown,
            reprs = lambda *args: "\n".join([repr(arg) for arg in args]),
            escape_str = escape_string,
            version = self._global_config.prompt_template.version or __version__,
            model_uid = self._model.uid,
            model_name = self._model.name,
            model_id = self._model.id,
            model_type = self._model.type.value,
            model_group = self._model.parent,
            botname = bot_name,
            username = self._user_info.username or "Unknown",
            nickname = self._user_info.nickname or "Unknown",
            user_age = self._user_info.age or "Unknown",
            user_gender = self._user_info.gender or "Unknown",
            user_info = self._user_info.model_dump(exclude_none=True),
            bot_birthday = f"{bot_birthday_year}-{bot_birthday_month}-{bot_birthday_day}",
            zodiac = lambda birthday_month = bot_birthday_month, birthday_day = bot_birthday_day: date_to_zodiac(int(birthday_month), int(birthday_day)),
            time = lambda time_format = "%Y-%m-%d(%A) %H:%M:%S %Z": format_timestamp(now, time_offset, time_format),
            age = lambda birthday_year = bot_birthday_year, birthday_month = bot_birthday_month, birthday_day = bot_birthday_day: calculate_age(
                int(birthday_year),
                int(birthday_month),
                int(birthday_day),
                offset_timezone = time_offset
            ),
            precise_age = lambda birthday_year, birthday_month, birthday_day, birthday_hour = None, birthday_minute = None, birthday_second = None: calculate_precise_age(
                int(birthday_year),
                int(birthday_month),
                int(birthday_day),
                int(birthday_hour) if birthday_hour is not None else None,
                int(birthday_minute) if birthday_minute is not None else None,
                int(birthday_second) if birthday_second is not None else None,
                offset_timezone = time_offset
            ),
            random = lambda min, max: random.randint(int(min), int(max)),
            randfloat = lambda min, max: random.uniform(float(min), float(max)),
            randchoice = lambda *args: random.choice(args),
            generate_uuid = lambda: uuid4(),
            copytext = lambda text, number, spacers = "": spacers.join([text] * int(number)),
            text_matrix = lambda text, columns, lines, spacers = " ", line_breaks = "\n": line_breaks.join(spacers.join([text] * int(columns)) for _ in range(int(lines))),
            random_matrix = lambda rows, cols: np.random.rand(int(rows), int(cols)),
            user_profile = lambda: self._config.user_profile if self._config.user_profile is not None else self._global_config.prompt_template.default_user_profile,
            user_configs = lambda indent = 4, ensure_ascii = False: json.dumps(self._config.model_dump(exclude_none=True), indent = int(indent), ensure_ascii = ensure_ascii),
            **kwargs
        )