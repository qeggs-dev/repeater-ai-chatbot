from pydantic import BaseModel, Field, ConfigDict
from ._preprocess_map import Preprocess_Map_Config

class Markdown_To_HTML_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_style: str = "light"
    styles_base_path: str = "/styles"
    style_file_encoding: str = "utf-8"
    html_template_base_path: str = "/html_templates"
    html_template_file_encoding: str = "utf-8"
    default_html_template: str = "standard"
    html_template_suffix: str = ".html"
    allow_custom_styles: bool = False
    allow_custom_html_templates: bool = False
    allow_direct_output: bool = False
    extensions: list[str] = [
        "extra",
        "sane_lists",
        "admonition",
        "codehilite"
    ]
    allowed_tags: list[str] = [
        "p", "br", "strong", "em", "u", "del", "ins",
        "h1", "h2", "h3", "h4", "h5", "h6",
        "ul", "ol", "li",
        "a", "img",
        "code", "pre", "blockquote",
        "table", "thead", "tbody", "tr", "th", "td",
    ]
    allowed_attrs: dict[str, list[str]] = {
        "a": ["href", "title", "rel"],
        "img": ["src", "alt", "title"],
        "code": ["class"],
        "pre": ["class"],
    }
    allowed_protocols: list[str] = ["http", "https", "mailto"]
    no_pre_labels: bool | None = False
    preprocess_map: Preprocess_Map_Config = Field(default_factory=Preprocess_Map_Config)
    title: str = "Repeater Image Generator"
    document_end_comments: str = ""