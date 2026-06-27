from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field
from jinja2 import Environment
from jinja2.sandbox import (
    SandboxedEnvironment,
    ImmutableSandboxedEnvironment,
)

class SandboxMode(StrEnum):
    """Sandbox mode for Jinja2 templates."""
    SANDBOXED = "sandboxed"
    IMMUTABLE_SANDBOXED = "immutable_sandboxed"
    NONE = "none"

class SandboxConfig(BaseModel):
    """Sandbox config for Jinja2 templates."""
    sandbox_mode: SandboxMode = SandboxMode.SANDBOXED

    def get_jinja_env(self) -> Environment:
        """Get Jinja2 environment based on sandbox mode."""
        match self.sandbox_mode:
            case SandboxMode.SANDBOXED:
                return SandboxedEnvironment(
                    enable_async = True,
                )
            case SandboxMode.IMMUTABLE_SANDBOXED:
                return ImmutableSandboxedEnvironment(
                    enable_async = True,
                )
            case SandboxMode.NONE:
                return Environment(
                    enable_async = True,
                )