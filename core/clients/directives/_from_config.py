from ._load_prompt_directives import load_prompt_directive
from ...user_config_manager import UserConfigs
from ...global_config_manager import GlobalConfigs
from typing import AsyncGenerator, Iterable

async def load_prompt_directive_from_config(
    base_type: Iterable[str],
    user_configs: UserConfigs,
    global_configs: GlobalConfigs
) -> AsyncGenerator[str, None]:
    if user_configs.prompt_directives is None:
        prompt_directives = global_configs.prompt.prompt_directives
    else:
        prompt_directives = user_configs.prompt_directives
    
    directives_names: list[tuple[str, str]] =  []

    for directive_type in base_type:
        if directive_type in prompt_directives:
            directives_names.extend(
                (
                    directive_type,
                    directive
                ) for directive in prompt_directives[directive_type]
            )

    for directive_type, directive_name in directives_names:
        yield await load_prompt_directive(
            directive_type,
            directive_name,
        )