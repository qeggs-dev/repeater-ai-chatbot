from yarl import URL
from ...runtime_container import RuntimeContainer
from ...global_config_manager import ConfigManager

async def load_prompt_directive(
    base_type: str,
    directive_name: str
):
    runtime = RuntimeContainer.get_runtime()
    config = ConfigManager.get_configs()

    base_path = config.prompt.directive_base_path
    static_client = runtime.static_resources_client

    directive_file = URL(base_path) / base_type / f"{directive_name}.md"
    directive_content = await static_client.get_text(directive_file)

    return directive_content