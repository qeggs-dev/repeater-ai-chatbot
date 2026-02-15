# User Data Type

用户的数据分为三种类型
- Context
- Prompt
- Config
这些数据以无缩进JSON的方式保存
以减少缩进数据对存储的占用

为了可读性，这里演示将按照 JSON 缩进格式化后展示

## Context

上下文数据，这种数据是一个JSON列表
元素是一个字典

格式如下：

```json
[
    {
        "role": "user",
        "content": "Hello?"
    },
    {
        "role": "assistant",
        "content": "Hi, how can I help you?"
    }
]
```

如你所见，Context 默认并不包含 System Role 消息段
这是为了方便我们处理与路由，这部分数据存储在 [Prompt](#Prompt) 数据中
当然，你仍然可以在中间穿插 System Role 消息
但你需要确保目标 API 能够支持这种结构的请求

## Prompt

Prompt 可以看作是一个特殊的 Context 单元
为了方便管理与路由，它会被独立存储
Prompt 分预设和用户自定义两种
用户自定义的 Prompt 存储在用户数据中，格式为 JSON 字符串
预设的 Prompt 通常存储在 `./configs/prompt/preset` 目录中，格式为 Markdown

用户存储的 Prompt 格式如下：

``` json
"You are a helpful assistant.\nYou are helpful, kind, and polite.\nNow: {{time()}}"
```

由于共享存储管理器，Prompt 的数据其实并不会存为 PlainText
而是以 JSON 格式存储在用户数据中

预设 Prompt 使用 Markdown 格式
相同内容的提示词格式如下：

``` markdown
You are a helpful assistant.
You are helpful, kind, and polite.
Now: {{time()}}
```

提示词通常建议使用 Markdown 格式
因为 LLM 通常会针对 Markdown 格式进行优化训练

Prompt 在预处理阶段会被拼接到 Context 的头部
并使用 System Role 保证 LLM 正确理解提示词

## Config

Config 是一个 JSON 字典
存储了一些用户自己的配置信息
它通常用于控制模型参数，指导处理流程等方面
字段详情请查看 [UserConfig](./../../configs/user_config.md)