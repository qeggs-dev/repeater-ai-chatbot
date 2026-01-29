# Render API

将 Markdown 文本转换为图片进行输出

- **`/render/{user_id:str}`**
  - **Requset**
    - **method:** `POST`
    - **type:** `JSON`
    - **Request Body**:
      - `text(str)` 要渲染的文本（必填）
      - `style(str)` 渲染风格
      - `image_expiry_time(float)` 图片链接有效时长
      - `css(str)` 自定义CSS
      - `html_template` HTML模板
      - `width(int)` 图片宽度
      - `height(int)` 图片高度
      - `direct_output(bool)` 是否直接开始渲染而不经过Markdown解析
      - `no_pre_labels(bool)` 是否不使用 &lt;pre&gt; 标签
      - `no_escape(bool)` 是否不转义 HTML 特殊字符
      - `quality(int)` 图片质量
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `image_url (str)` 图片渲染输出文件URL
      - `file_uuid (str)` 图片渲染输出文件的UUID
      - `style (str)` 渲染风格，如果使用了自定义CSS则返回`custom`
      - `status (str)` 渲染处理器的状态，只有`success`,`failed`和`pending`三种状态
      - `browser_used (str)` 渲染使用的浏览器
      - `url_expiry_time (float)` 图片链接有效时长
      - `error (str)` 渲染错误信息
      - `text (str)` 渲染的文本
      - `image_render_time_ms (float)` 图片渲染时间（毫秒）
      - `created (int)` 图片渲染输出文件的创建时间戳
      - `created_ms (int)` 图片渲染输出文件的创建时间戳（毫秒）
      - `details_time`
          - `preprocess (int)` 预处理时间（纳秒）
          - `markdown_to_html (int)` Markdown 到 HTML 的转译耗时（纳秒）
          - `render (int)` HTML 渲染耗时（纳秒）

注：该API中的`html_template`含有一些嵌入变量
使用了[变量展开引擎](../template_expansion_engine/main.md)进行处理
目前支持的变量如下
- `{html_content}` 转换后的HTML内容
- `{css}` 自定义或预设的CSS内容
- `{markdown}` 经过HTML转义后的Markdown文本内容
- `{title}` 页面标题

其中除了`{css}`
其他变量都经历了HTML转义处理
但你仍然需要**保证你的HTML模板和CSS是可信任的**
否则攻击者可能会通过它们进行XSS攻击，注入恶意代码