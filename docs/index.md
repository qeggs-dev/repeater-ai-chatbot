# 详细配置

下面，请您按照您的需求查阅详细配置文档

---

## 环境变量

[环境变量表](./envs.md)

---

## 配置文件

- [Main Config](./configs/main.md)
- [API_INFO](./configs/api_info.md)
- [Blacklist](./configs/blacklist.md)
- [User_Nickname_Mapping](./configs/uer_nickname_mapping.md)

用于管理程序的运行行为
以及模型资源等内容

---

## 用户配置

请参阅：[用户配置](./configs/user_config.md).
注：用户配置不属于部署配置
这个部分只有你需要为其进行 Client 开发时才需要用到

---

## Repeater API

请参阅：[Repeater API](./api_table/index.md)
如果你正在使用已经开发好的 Client
那么这个章节就不是给你准备的

---

## Markdown图片渲染

- [Markdown图片渲染模板](./markdown_render/template.md)
- [Markdown图片渲染样式](./markdown_render/style.md)

---

## Prompt

该项目在 `configs/prompt/presets` 目录中
提供了多个预设的Prompt
这些预设的 Prompt 与该项目一同使用 MIT 许可证发布
这里面的预设可能会在不同版本里有所变动
非常建议用户在拿到后，先创建一份自己的 Prompt

---

## 模板展开系统

项目中提供了模板展开系统
用于对提示词模板和用户输入模板进行变量展开
充分利用好模板展开器，可以实现很多有趣的功能
详情请参阅：[模板展开系统](./template_expansion_engine/main.md)

---

## 多模态输入

在 `/chat/completion` 端点下面
传入 `image_url` 即可让后端构造视觉模态请求
但需要保证目标模型支持视觉模态输入
其他模态还请等待后续更新

---

## 版本号规则

请参阅：[版本号系统](./version.md)
你需要确保 Client 支持当前 Repeater 的版本
否则可能会出现接口不兼容的问题