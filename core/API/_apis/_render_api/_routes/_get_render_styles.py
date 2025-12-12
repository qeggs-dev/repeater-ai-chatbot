from ...._resource import (
    app
)
from .....Markdown_Render import (
    Styles,
)
from fastapi.responses import ORJSONResponse
from pathlib import Path
from .....Global_Config_Manager import ConfigManager

@app.get("/render_styles")
async def get_render_styles():
    styles_path = Path(ConfigManager.get_configs().render.markdown.styles_dir)
    styles = Styles(
        styles_path = styles_path,
    )
    style_names = styles.get_style_names()
    return ORJSONResponse(style_names)