import html
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
    title: str = "Markdown Render",
    width: int = 800,
    direct_output: bool = False,
    no_escape: bool = False,
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
    
    # 2. 转义以安全包含内容
    if not no_escape:
        input_text = html.escape(input_text)
    
    # 3. 渲染 Markdown 为 HTML
    if not direct_output:
        html_content = markdown.markdown(
            input_text,
            extensions=[
                CodeBlockExtension(),
                BrExtension(),
                DividingLineExtension(),
            ]
        )
    else:
        if no_pre_labels:
            html_content = input_text
        else:
            html_content = f"<pre>\n{input_text}\n</pre>"

    # 4. 预处理 HTML 文本
    if preprocess_map_after:
        for key, value in preprocess_map_after.items():
            html_content = html_content.replace(key, value)
    
    # 5. 添加自适应宽度
    css += f"\nbody {{ width: {max(width, 60) - 60}px; }}"

    template: Template = environment.from_string(html_template)

    full_html = await asyncio.to_thread(
        template.render,
        markdown = html.escape(input_text),
        raw_text = input_text,
        html_content = html_content,
        css = css,
        document_end_comments = document_end_comments,
        title = html.escape(title)
    )
    
    return full_html