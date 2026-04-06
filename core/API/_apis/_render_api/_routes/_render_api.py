import time
import aiofiles

from ...._resource import Resource
from .....Markdown_Render import (
    markdown_to_html,
)
from fastapi.responses import ORJSONResponse
from loguru import logger
from uuid import uuid4
from pathlib import Path
from yarl import URL
from .....Global_Config_Manager import ConfigManager
from .....Lifespan import (
    ExitHandler
)
from .....Delayed_Tasks_Pool import DelayedTasksPool
from .._assists import (
    get_style
)
from .._requests import (
    RenderRequest
)
from .._responses import (
    Render_Response,
    RenderTime
)
from .....SpecialException import HTTPException

delayed_tasks_pool = DelayedTasksPool()
ExitHandler.add_function(delayed_tasks_pool.cancel_all())

@Resource.app.post("/render/{user_id}")
async def render(
    user_id: str,
    request:RenderRequest
):
    """
    Endpoint for rendering markdown text to image
    """
    start_time = time.monotonic_ns()

    global_configs = ConfigManager.get_configs()

    # 检查请求是否合法
    if not request.text:
        raise HTTPException(status_code=400, message="text is required")
    
    if request.direct_output and not global_configs.render.markdown.allow_direct_output:
        raise HTTPException(status_code=400, message="direct_output is not allowed")
    
    if request.style and not global_configs.render.markdown.allow_custom_styles:
        raise HTTPException(status_code=400, message="custom style is not allowed")
    
    if request.html_template and not global_configs.render.markdown.allow_custom_html_templates: 
        raise HTTPException(status_code=400, message="custom html_template is not allowed")
    
    # 获取用户配置
    config = await Resource.core.user_config_manager.load(user_id)
        
    style_name, css = await get_style(
        request = request,
        user_configs = config,
        static_resources_client = Resource.core.static_resources_client,
    )
    
    if not request.image_expiry_time:
        render_url_expiry_time = global_configs.render.default_image_timeout
    else:
        render_url_expiry_time = request.image_expiry_time
    
    # 日志打印文件名和渲染风格
    logger.info(
        "Rendering image for \"{style_name}\" style",
        user_id = user_id,
        style_name = style_name
    )

    preprocess_map_before = global_configs.render.markdown.preprocess_map.before
    preprocess_map_after = global_configs.render.markdown.preprocess_map.after
    html_template_dir = URL(global_configs.render.markdown.html_template_base_path)
    html_template_encoding = global_configs.render.markdown.html_template_file_encoding
    html_template_name = config.render_html_template if config.render_html_template is not None else global_configs.render.markdown.default_html_template
    html_template_suffix = global_configs.render.markdown.html_template_suffix
    title = config.render_title if config.render_title is not None else global_configs.render.markdown.title

    width = request.width if request.width is not None else global_configs.render.markdown.width
    if request.document_bottom_comment:
        document_bottom_comment = request.document_bottom_comment
    else:
        document_bottom_comment = config.render_document_bottom_comment if config.render_document_bottom_comment is not None else global_configs.render.markdown.document_bottom_comment
    environment = global_configs.text_template.sandbox.get_jinja_env()

    base_url = global_configs.render.to_image.base_url

    no_pre_labels = global_configs.render.markdown.no_pre_labels
    if no_pre_labels is None:
        no_pre_labels = request.no_pre_labels

    allowed_tags = global_configs.render.markdown.allowed_tags
    allowed_attrs = global_configs.render.markdown.allowed_attrs
    allowed_protocols = global_configs.render.markdown.allowed_protocols

    markdown_extensions = global_configs.render.markdown.extensions

    # 读取HTML模板
    if request.html_template is not None:
        html_template = request.html_template
    else:
        html_template_file = html_template_dir / f"{html_template_name}{html_template_suffix}"
        html_template = await Resource.core.static_resources_client.get_text(
            html_template_file,
            text_encoding = html_template_encoding
        )
    
    end_of_preprocessing = time.monotonic_ns()

    # 调用生成HTML
    html = await markdown_to_html(
        input_text = request.text,
        html_template = html_template,
        environment = environment,
        width = width,
        title = title,
        css = css,
        style_name = style_name,
        direct_output = request.direct_output,
        markdown_extensions = markdown_extensions,
        allowed_tags = allowed_tags,
        allowed_attrs = allowed_attrs,
        allowed_protocols = allowed_protocols,
        no_pre_labels = no_pre_labels,
        document_bottom_comment = document_bottom_comment,
        preprocess_map_before = preprocess_map_before,
        preprocess_map_after = preprocess_map_after,
    )

    end_of_md_to_html = time.monotonic_ns()

    # 生成图片
    response = await Resource.html_render_client.render(html)
    result = response.get_data()
    if result is None:
        raise HTTPException(status_code=500, message="The response data could not be obtained correctly.")
    
    fileurl = result.image_url

    create_ms = result.created_ms
    created = result.created

    end_of_render = time.monotonic_ns()

    return ORJSONResponse(
        Render_Response(
            image_url = fileurl,
            file_uuid = result.file_uuid,
            style = style_name,
            url_expiry_time = render_url_expiry_time,
            text = request.text,
            created = created,
            created_ms = create_ms,
            details_time = RenderTime(
                preprocess = end_of_preprocessing - start_time,
                markdown_to_html = end_of_md_to_html - end_of_preprocessing,
                render = end_of_render - end_of_md_to_html
            )
        ).model_dump(
            exclude_none = True
        )
    )

