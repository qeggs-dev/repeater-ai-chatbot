from pydantic import BaseModel, ConfigDict, field_validator, Field
from zoneinfo import ZoneInfo, available_timezones
from typing import Any

class UserConfigs(BaseModel):
    """
    Configs for user.
    """
    model_config = ConfigDict(
        case_sensitive=False,
        validate_assignment=True
    )

    parset_prompt_name: str | None = None
    model_uid: str | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    top_p: float | None = Field(None, ge=0.0, le=1.0)
    max_tokens: int | None = None
    max_completion_tokens: int | None = None
    stop: list[str] | None = None
    frequency_penalty: float | None = Field(None, ge=-2.0, le=2.0)
    presence_penalty: float | None = Field(None, ge=-2.0, le=2.0)
    context_shrink_limit: int | None = None
    render_style: str | None = None
    render_html_template: str | None = None
    render_title: str | None = None
    load_prompt: bool = True
    save_context: bool = True
    user_profile: str | None = None
    timezone: float | str | None = None
    save_text_only: bool | None = True
    appending_user_data: dict[str, Any] = Field(default_factory=dict)

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
        elif v is None:
            pass
        else:
            raise ValueError("Invalid time offset type")
        return v