from pydantic import BaseModel, ConfigDict, field_validator, Field
from zoneinfo import ZoneInfo, available_timezones

class Time_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    timezone: str | float = "UTC"

    @field_validator("timezone")
    def check_timezone(cls, v):
        if isinstance(v, str):
            if v not in available_timezones():
                raise ValueError(f"Invalid time zone {v}")
        elif isinstance(v, ZoneInfo):
            pass
        elif isinstance(v, int) or isinstance(v, float):
            if not -12 <= v <= 14:
                raise ValueError(f"Invalid time offset {v}")
        else:
            raise ValueError("Invalid time offset type")
        return v