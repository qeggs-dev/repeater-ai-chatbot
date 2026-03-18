import json
import random
import secrets
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
from datetime import datetime, timedelta, timezone
from TimeParser import (
    get_timezone_offset,
    calculation_date_countdown,
    format_time_duration,
    date_to_zodiac,
    tz_timestamp,
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
            user_config: UserConfigs = UserConfigs(),
        ):
        self._model = model
        self._user_info = user_info
        self._global_config = global_config
        self._user_config = user_config

    def render(
            self,
            text: str,
            /,
            **kwargs: Any
        ) -> str:
        try:
            environment = self._global_config.text_template.sandbox.get_jinja_env()
            template: Template = environment.from_string(
                source = text
            )
            return template.render(
                **kwargs,
            )
        except Exception as e:
            logger.error(
                "Template Render Error: {error}",
                error = e
            )
            raise
        

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
        tz_config = self._user_config.timezone
        if tz_config is None:
            tz_config = self._global_config.text_template.time.timezone
        
        now = datetime.now()

        if isinstance(tz_config, str):
            tz_offset = get_timezone_offset(
                timezone = tz_config,
                dt = now
            )
        else:
            tz_offset = timedelta(hours=tz_config)
        
        tz_now = tz_timestamp(
            timestamp = now,
            offset_timezone = tz_offset
        )
        
        def date_countdown(
                target_month:int,
                target_day:int,
                target_hour:int | None = None,
                target_minute:int | None = None,
                target_second:int | None = None,
                precise: bool = False,
                time_delta_output: bool = False,
            ) -> str | timedelta:
            time_delta = calculation_date_countdown(
                target_month = target_month,
                target_day = target_day,
                target_hour = target_hour,
                target_minute = target_minute,
                target_second = target_second,
                current_timestamp = tz_now,
                tz_offset = timezone(tz_offset),
            )
            
            if time_delta_output:
                return time_delta
            elif precise:
                return format_time_duration(time_delta.total_seconds(), use_abbreviation=True)
            else:
                return f"{time_delta.days} days"
        
        default_time_format = self._global_config.text_template.time.time_format

        daily_random = random.Random(
            tz_now.year ^ tz_now.month ^ tz_now.day
        )
        
        return self.render(
            text,
            user_id = user_id,
            date_countdown = date_countdown,
            escape_str = escape_string,
            version = self._global_config.text_template.version or __version__,
            model_uid = self._model.uid,
            model_name = self._model.name,
            model_id = self._model.id,
            model_type = self._model.type.value,
            model_group = self._model.parent,
            user_name = self._user_info.username or "",
            nick_name = self._user_info.nickname or "",
            user_age = self._user_info.age or "",
            user_gender = self._user_info.gender or "",
            user_custom_name = self._user_config.user_name,
            user_info = self._user_info.model_dump(exclude_none=True),
            zodiac = date_to_zodiac,
            time = lambda time_format = default_time_format: tz_now.strftime(time_format),
            now = tz_now,
            age = lambda birthday_year, birthday_month, birthday_day: calculate_age(
                int(birthday_year),
                int(birthday_month),
                int(birthday_day),
                current_timestamp = tz_now
            ),
            precise_age = lambda birthday_year, birthday_month, birthday_day, birthday_hour = None, birthday_minute = None, birthday_second = None: calculate_precise_age(
                int(birthday_year),
                int(birthday_month),
                int(birthday_day),
                int(birthday_hour) if birthday_hour is not None else None,
                int(birthday_minute) if birthday_minute is not None else None,
                int(birthday_second) if birthday_second is not None else None,
                current_timestamp = tz_now
            ),
            random = lambda min, max: random.randint(int(min), int(max)),
            randfloat = lambda min, max: random.uniform(float(min), float(max)),
            randchoice = lambda *args: random.choice(args),
            daily_random = lambda min, max: daily_random.randint(int(min), int(max)),
            daily_randfloat = lambda min, max: daily_random.uniform(float(min), float(max)),
            daily_randchoice = lambda *args: daily_random.choice(args),
            secrets_random = secrets.randbelow,
            secrets_randbits = secrets.randbits,
            secrets_token_hex = secrets.token_hex,
            secrets_token_urlsafe = secrets.token_urlsafe,
            secrets_token_bytes = secrets.token_bytes,
            secrets_random_choice = lambda *args: secrets.choice(args),
            generate_uuid = lambda: uuid4(),
            copy_text = lambda text, number, spacers = "": spacers.join([text] * int(number)),
            text_matrix = lambda text, columns, lines, spacers = " ", line_breaks = "\n": line_breaks.join(spacers.join([text] * int(columns)) for _ in range(int(lines))),
            random_matrix = np.random.rand,
            user_profile = self._user_config.user_profile if self._user_config.user_profile is not None else self._global_config.text_template.default_user_profile,
            user_configs = self._user_config.model_dump(exclude_none=True),
            json_loads = json.loads,
            json_dumps = json.dumps,
            **kwargs
        )