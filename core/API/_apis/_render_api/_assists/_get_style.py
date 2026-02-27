from .._requests import RenderRequest
from .....Global_Config_Manager import ConfigManager
from .....Markdown_Render import Styles
from .....User_Config_Manager import UserConfigs
from fastapi import HTTPException

async def get_style(request: RenderRequest, user_configs: UserConfigs):
    """
    获取用户配置的样式文件

    :param request: 请求参数
    :param user_configs: 用户配置
    :return: 样式文件内容(样式名称，样式文件内容)
    """
    style_path = ConfigManager.get_configs().render.markdown.styles_dir
    styles = Styles(
        style_path
    )
    style_file_encoding = ConfigManager.get_configs().render.markdown.style_file_encoding

    if request.css:
        style_name = "custom"
        css = request.css
    elif request.style:
        if request.style in styles.get_style_names():
            style_name = request.style
        else:
            raise HTTPException(
                status_code=404,
                detail="Style not found"
            )
        
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
        
        css = await styles.get_style(
            style_name,
            encoding = style_file_encoding
        )
    
    return style_name, css