from ...._resource import Resource
from .....Markdown_Render import (
    markdown_to_html,
    Styles,
    HTML_Render
)
from fastapi import (
    HTTPException,
    Request
)
from fastapi.responses import ORJSONResponse
import aiofiles
import time
from loguru import logger
from uuid import uuid4
from pathlib import Path
from .....Global_Config_Manager import ConfigManager
from .....Lifespan import (
    ExitHandler
)
from .....Delayed_Tasks_Pool import DelayedTasksPool
from .._assists import (
    delete_image,
    get_style
)
from .._requests import (
    RenderRequest
)
from .._responses import (
    Render_Response,
    RenderTime
)

delayed_tasks_pool = DelayedTasksPool()
ExitHandler.add_function(delayed_tasks_pool.cancel_all())

@Resource.app.post("/render/{user_id}")
async def render(
    request: Request,
    user_id: str,
    render_request:RenderRequest
):
    """
    Endpoint for rendering markdown text to image
    """
    start_time = time.monotonic_ns()

    if not render_request.text:
        raise HTTPException(status_code=400, detail="text is required")
    
    if render_request.direct_output and not ConfigManager.get_configs().render.markdown.allow_direct_output:
        raise HTTPException(status_code=400, detail="direct_output is not allowed")
    
    # 生成图片ID
    fuuid = uuid4()
    filename = f"{fuuid}{ConfigManager.get_configs().render.to_image.output_suffix}"
    render_output_image_dir = Path(ConfigManager.get_configs().render.to_image.output_dir)
    
    # 获取用户配置
    config = await Resource.core.user_config_manager.load(user_id)
        
    style_name, css = await get_style(
        user_id = user_id,
        request = render_request,
        user_configs = config
    )
    
    if not render_request.image_expiry_time:
        render_url_expiry_time = ConfigManager.get_configs().render.default_image_timeout
    else:
        render_url_expiry_time = render_request.image_expiry_time
    
    # 日志打印文件名和渲染风格
    logger.info(f"Rendering image {filename} for \"{style_name}\" style", user_id=user_id)

    browser_type = ConfigManager.get_configs().render.to_image.browser_type
    preprocess_map_before = ConfigManager.get_configs().render.markdown.preprocess_map.before
    preprocess_map_after = ConfigManager.get_configs().render.markdown.preprocess_map.after
    html_template_dir = Path(ConfigManager.get_configs().render.markdown.html_template_dir)
    html_template_encoding = ConfigManager.get_configs().render.markdown.html_template_file_encoding
    html_template_name = config.render_html_template if config.render_html_template is not None else ConfigManager.get_configs().render.markdown.default_html_template
    html_template_suffix = ConfigManager.get_configs().render.markdown.html_template_suffix
    title = config.render_title if config.render_title is not None else ConfigManager.get_configs().render.markdown.title

    width = render_request.width if render_request.width is not None else ConfigManager.get_configs().render.to_image.width
    height = render_request.height if render_request.height is not None else ConfigManager.get_configs().render.to_image.height
    quality = render_request.quality if render_request.quality is not None else ConfigManager.get_configs().render.to_image.quality
    no_pre_labels = ConfigManager.get_configs().render.markdown.no_pre_labels
    if no_pre_labels is None:
        no_pre_labels = render_request.no_pre_labels
    no_escape = ConfigManager.get_configs().render.markdown.no_escape
    if no_escape is None:
        no_escape = render_request.no_escape

    # 读取HTML模板
    if render_request.html_template is not None:
        html_template = render_request.html_template
    else:
        htmp_temllate_file = html_template_dir / f"{html_template_name}{html_template_suffix}"
        if not htmp_temllate_file.exists():
            raise ORJSONResponse(
                content = Render_Response(
                    error = f"HTML template file not found"
                ).model_dump(exclude_none=True),
                status_code= 404
            )
        async with aiofiles.open(
            htmp_temllate_file,
            "r",
            encoding = html_template_encoding
        ) as f:
            html_template = await f.read()
    
    end_of_preprocessing = time.monotonic_ns()

    # 调用生成HTML
    html = await markdown_to_html(
        input_text = render_request.text,
        html_template = html_template,
        width = width,
        title = title,
        css = css,
        direct_output = render_request.direct_output,
        no_escape = no_escape,
        no_pre_labels = no_pre_labels,
        preprocess_map_before = preprocess_map_before,
        preprocess_map_after = preprocess_map_after,
    )

    end_of_md_to_html = time.monotonic_ns()

    # 生成图片
    result = await Resource.browser_pool_manager.render_html(
        html_content = html,
        output_path = str(render_output_image_dir / filename),
        browser_type = browser_type,
        config = HTML_Render.RenderConfig(
            width = width,
            height = height,
            quality = quality
        )
    )

    end_of_render = time.monotonic_ns()

    create_ms = time.time_ns() // 10**6
    create = create_ms // 1000
    logger.info(f"Created image {filename}", user_id = user_id)

    # 添加一个后台任务，时间到后删除图片
    await delayed_tasks_pool.add_task(
        render_url_expiry_time,
        delete_image(
            user_id = user_id,
            render_output_image_dir = render_output_image_dir,
            filename = filename
        ),
        id = "Markdown Render Image Timing Deleter"
    )

    # 生成图片的URL
    fileurl = request.url_for("render_file", file_uuid=fuuid)

    return ORJSONResponse(
        Render_Response(
            image_url = str(fileurl),
            file_uuid = str(fuuid),
            style = style_name,
            status = result.status,
            browser_used = result.browser_used,
            url_expiry_time = render_url_expiry_time,
            error = result.error,
            text = render_request.text,
            image_render_time_ms = result.render_time_ms,
            created = create,
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

