# API_INFO 模型配置文件

此配置用于告诉 Repeater 有哪些可用模型
它们的 API Key 在哪里
以及它们向内部显示的模型UID

PS：`Model UID` 是 Repeater 内部使用的唯一标识符，用于区分不同的模型
也是用户在切换模型时需要写的参数
`Model UID` 和 `Model Type` 共同组成了查询键
`Model Type` 的详细描述请查看 [模型类型](../model_type.md)
用户在调用 `主API` 的时候，会查询 "chat" 类型的模型
而 `模型ID` 则是调用 `API` 时实际使用的模型ID

```json
[
    {
        "name": "Deepseek", // 显示在日志上的模型组名称
        "api_key_env": "DEEPSEEK_API_KEY", // 这里填写API_KEY的环境变量名称
        "url": "https://api.deepseek.com", // 这里填写API的URL
        "models": [
            {
                "name": "Deepseek Think Model", // 显示在日志上的模型名称
                "id": "deepseek-reasoner", // 面向 API厂商 的 模型ID
                "uid": "deepseek-reasoner", // 面向 Repeater 和 用户 的 模型ID
                "type": "chat" // 模型类型，用于告诉Repeater这个模型可以干什么
            },
            {
                "name": "Deepseek Chat Model",
                "id": "deepseek-chat",
                "uid": "deepseek-chat",
                "url": "https://api.deepseek.com/chat", // 如果模型有单独的URL，可以单独填写
                "type": "chat"
            }
        ]
    },
    {
        "name": "Open AI",
        "api_key_env": "OPENAI_API_KEY",
        "url": "https://api.openai.com/v1",
        "models": [
            {
                "name": "GPT-3.5 Turbo",
                "id": "gpt-3.5-turbo",
                "uid": "gpt-3.5-turbo",
                "type": "chat"
            },
            {
                "name": "GPT-4",
                "id": "gpt-4",
                "uid": "gpt-4",
                "timeout": 240.0, // 模型单独设置的超时时间可以覆盖模型组提供的全局设置
                "type": "chat"
            }
        ],
        "timeout": 120.0 // 请求的超时设置，单位为秒
    }
]
```
YAML同理
解析器可以解析yaml格式的文件
它通过后缀名的方式进行识别
并使用不同的反序列化函数