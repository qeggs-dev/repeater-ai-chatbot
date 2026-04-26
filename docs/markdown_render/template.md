# Markdown图片渲染模板

渲染模板的本体是一个 HTML 文件
它默认存放在 `./configs/html_templates` 目录下
你可以通过 `render.markdown.html_template_dir` 这个全局配置来修改路径

---

## 模板变量

| 变量名 | 类型 | 描述 |
| --- | --- | --- |
| `html_content` | `string` | Markdown 渲染后的 HTML 内容 |
| `adaptive_width_css` | `string` | 自适应宽度的 CSS 样式 |
| `title` | `string` | 一个自定义的标题<br/>由 用户配置`render_title` 和<br/>全局配置`render.markdown.title` 定义<br/>通常被放在页面顶部 |
| `css_url` | `string or null` | 用户选择或传入的 CSS 文件 URL |
| `html_template_url` | `string or null` | 用户选择或传入的 HTML 模板文件 URL |
| `markdown` | `string` | 传入的 Markdown 内容(经过 HTML 转义) |
| `raw_text` | `string` | 传入的原始内容 |
| `document_bottom_comment` | `string` | 用户配置或传入的文档末尾注释 |

这些内容使用了 [模板展开器](../template_engine/main.md) 来进行展开
模板变量的展开规则和 [模板展开器](../template_engine/main.md) 一致
但并未使用到 [模板变量](../template_engine/variables.md) 中的内容