import html
import bleach
import asyncio
import markdown

from ._extensions import (
    BrExtension,
    CodeBlockExtension,
    DividingLineExtension
)
from jinja2 import Template, Environment

async def markdown_to_html(
    input_text: str,
    html_template: str,
    environment: Environment,
    css: str,
    style_name: str,
    title: str = "Markdown Render",
    width: int = 800,
    markdown_extensions: list[str | markdown.Extension] | None = None,
    direct_output: bool = False,
    allowed_tags: bool = False,
    allowed_attrs: bool = False,
    allowed_protocols: bool = False,
    no_pre_labels: bool = False,
    document_end_comments: bool = False,
    preprocess_map_before: dict[str, str] | None = None,
    preprocess_map_after: dict[str, str] | None = None,
) -> str:
    """
    使用 wkhtmltoimage 将 Markdown 转为 HTML
    
    参数:
    - markdown_text: Markdown 文本
    - html_template: HTML 模板内容
    - css: 自定义 CSS 样式 (优先级高于style参数)
    - title: HTML 文档标题
    - width: 目标宽度 (像素)
    - direct_output: 是否直接输出 HTML 文本
    - no_escape: 是否不转义 HTML 特殊字符
    - no_pre_labels: 是否不添加自动添加 pre 标签
    - preprocess_map_before: 渲染前自定义字符映射
    - preprocess_map_after: 渲染后自定义字符映射
    
    返回: 输出文件路径
    """
    # 1. 预处理 Markdown 文本
    if preprocess_map_before:
        for key, value in preprocess_map_before.items():
            input_text = input_text.replace(key, value)
    
    # 2. 渲染 Markdown 为 HTML
    if not direct_output:
        extensions = [
            CodeBlockExtension(),
            DividingLineExtension(),
        ]
        if markdown_extensions:
            extensions.extend(markdown_extensions)
        html_content = markdown.markdown(
            input_text,
            extensions = extensions,
        )
    else:
        if no_pre_labels:
            html_content = input_text
        else:
            html_content = f"<pre>\n{input_text}\n</pre>"
    
    # 3. 清理不允许的 HTML 文本
    clean_html = bleach.clean(
        html_content,
        tags = allowed_tags,
        attributes = allowed_attrs,
        protocols = allowed_protocols,
        strip = True,  # 移除不允许的标签
        strip_comments = True  # 移除注释
    )

    # 4. 预处理 HTML 文本
    if preprocess_map_after:
        for key, value in preprocess_map_after.items():
            clean_html = clean_html.replace(key, value)
    
    # 5. 添加自适应宽度
    css += f"\nbody {{ width: {max(width, 60) - 60}px; }}"

    template: Template = environment.from_string(html_template)

    full_html = await asyncio.to_thread(
        template.render,
        markdown = html.escape(input_text),
        raw_text = input_text,
        html_content = clean_html,
        css = css,
        style_name = html.escape(style_name),
        document_end_comments = document_end_comments,
        title = html.escape(title)
    )
    
    return full_html