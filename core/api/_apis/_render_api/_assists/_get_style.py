from .._requests import RenderRequest
from .....global_config_manager import ConfigManager
from .....markdown_render import Styles
from .....user_config_manager import UserConfigs
from .....static_resources_client import StaticResourcesClient

async def get_style(request: RenderRequest, user_configs: UserConfigs, static_resources_client: StaticResourcesClient):
    """
    获取用户配置的样式文件

    :param request: 请求参数
    :param user_configs: 用户配置
    :return: 样式文件内容(样式名称，样式文件内容)
    """
    style_path = ConfigManager.get_configs().render.markdown.styles_base_path
    styles = Styles(
        static_resources_client = static_resources_client,
        style_base_path = style_path
    )
    style_file_encoding = ConfigManager.get_configs().render.markdown.style_file_encoding

    if request.css:
        style_name = "custom"
        css = request.css
        style_url = None
    elif request.style:
        style_name = request.style
        style_url = styles.get_style_url(style_name)
        css = await styles.get_style(
            style_name,
            encoding = style_file_encoding
        )
    else:
        # 获取配置中的默认图片渲染风格
        if user_configs.render_style:
            style_name = user_configs.render_style
        else:
            style_name = ConfigManager.get_configs().render.markdown.default_style
        
        style_url = styles.get_style_url(style_name)
        css = await styles.get_style(
            style_name,
            encoding = style_file_encoding
        )
    
    return style_name, css, style_url