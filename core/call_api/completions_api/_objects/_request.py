from pydantic import BaseModel, Field, ConfigDict
from typing import Callable, Any
from ._delta import Delta
from ._stream_options import StreamOptions
from ....context_manager import (
    ContentRole
)
from ....context_manager.objects.function_calling import FunctionCaller

from ....context_manager import ContextObject

class Request(BaseModel):
    """
    This class is used to store the request data
    """
    model_config = ConfigDict(
        validate_assignment = True
    )

    url: str = ""
    key: str = ""
    model: str = ""
    user_name: str | None = None
    temperature: float = 1.0
    top_p: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    max_tokens: int = 0
    max_completion_tokens: int = 0
    timeout: float = 600.0
    stream: bool = False
    thinking: bool | None = None
    stop: list[str] | None = None
    context: ContextObject | None = None
    prompt: str | None = None
    echo: bool = False
    suffix: str | None = None
    remove_reasoning_prompt: bool = True
    logprobs: bool = False
    top_logprobs: int | None = None
    print_chunk: bool = True
    output_role: ContentRole = ContentRole.ASSISTANT
    tools: list[dict[str, Any]] | None = None
    tool_choice: str | dict[str, dict[str, str]] | None = None
    continue_processing_callback_function: Callable[[str, Delta], bool] | None = None
    stream_options: StreamOptions = Field(default_factory=StreamOptions)