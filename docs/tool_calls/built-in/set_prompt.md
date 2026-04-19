# Set Prompt Tool

设置提示词

注册名：`set_prompt`

AI 在调用该工具时，会传递以下参数：
```json
{
  "prompt": "..." // 提示词内容
}
```

该工具会主动尝试写入用户自定义提示词内容
模型自定义的提示词内容可被数据操作 API 所修改

然后返回 `Prompt seted.`