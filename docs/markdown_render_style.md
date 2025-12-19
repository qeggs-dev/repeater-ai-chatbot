# Markdown图片渲染样式

当 Repeater 想要将 Markdown 渲染成图片时
可以通过配置对使用的 CSS 进行路由
在全局配置中，这个字段是 `render.markdown.default_style`
在用户配置中，这个字段是 `render_style`
用户配置总会优先使用
而在用户配置未定义的情况下
会使用全局配置进行兜底

| 风格 | 译名 |
| --- | :---: |
| **`light`** | 亮色 |
| `dark` | 暗色 |
| `red` | 红色 |
| `pink` | 粉色 |
| `blue` | 蓝色 |
| `green` | 绿色 |
| `purple` | 紫色 |
| `yellow` | 黄色 |
| `orange` | 橙色 |
| `dark-red` | 暗红色 |
| `dark-pink` | 暗粉色 |
| `dark-blue` | 暗蓝色 |
| `dark-green` | 暗绿色 |
| `dark-purple` | 暗紫色 |
| `dark-yellow` | 暗黄色 |
| `dark-orange` | 暗橙色 |
| `legacy` | 旧版亮色 |
| `legacy-dark` | 旧版暗色 |
| `legacy-red` | 旧版红色 |
| `legacy-pink` | 旧版粉色 |
| `legacy-blue` | 旧版蓝色 |
| `legacy-green` | 旧版绿色 |
| `legacy-purple` | 旧版紫色 |
| `legacy-yellow` | 旧版黄色 |
| `legacy-orange` | 旧版橙色 |
| `legacy-dark-red` | 旧版暗红色 |
| `legacy-dark-pink` | 旧版暗粉色 |
| `legacy-dark-blue` | 旧版暗蓝色 |
| `legacy-dark-green` | 旧版暗绿色 |
| `legacy-dark-purple` | 旧版暗紫色 |
| `legacy-dark-yellow` | 旧版暗黄色 |
| `legacy-dark-orange` | 旧版暗橙色 |

颜色风格默认在 `./configs/style` 文件夹下
可以通过 `render.markdown.styles_dir` 这个全局配置来修改