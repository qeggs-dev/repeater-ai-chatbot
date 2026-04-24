# 用户配置文件

用户配置并不是一个运营应该接触的文件
它是一个由程序自动生成和管理的文件
通常你**不需要**也**不应该**手动修改它
它在用户数据目录下的config类型中
每个用户各有一个自己的配置文件
并且受到分支调控管理

不过如果你正在开发Client
那么你可能需要学习一下字段的含义
并通过接口来修改它们

```json
{
    
    // (str) 预设提示词
    // 用于快速路由定义好的提示词文件
    "preset_prompt_name": null,

    // (str | list[str]) 模型UID
    // 用于指定消息处理模型
    // 允许指定多个模型
    "model_uid": null,

    // (float) 模型温度参数
    // 温度越高模型输出的随机性就越高
    "temperature": null,

    // (float) 模型Top-p参数
    // Top-p参数越低
    // 模型在采样的时候就更倾向于使用更高概率的词
    "top_p": null,

    // (int) 最大生成长度
    // 模型新生成的文本长度不能超过这个值
    "max_tokens": null,

    // (int) 模型最大生成长度
    // 模型生成文本长度不能超过这个值
    "max_completion_tokens": null,

    // (list[str]) 模型停止生成文本的标志词
    // 当生成的文本中包含这些词时
    // 模型会停止生成
    "stop": null,

    // (bool) 是否让混合推理模型开启思考模式
    // 开启后模型会输出 CoT 思考内容
    // 仅对支持的模型生效
    "thinking": null,

    // (int | float) 模型生成超时
    // 当模型的生成时间超过该值时
    // 模型会停止生成
    // 如果为 null 则使用模型的默认超时
    "model_timeout": null,

    // (float) 模型频率惩罚参数
    // 频率惩罚参数越高
    // 模型在生成文本时越倾向于使用新的词
    "frequency_penalty": null,

    // (float) 模型存在性惩罚参数
    // 存在性惩罚参数越高
    // 模型越倾向于讨论新话题
    "presence_penalty": null,

    // (int) 定义上下文问的极限字数
    // Repeater会以一对消息为单位去删除过多的部分。
    "context_shrink_limit": null,

    // (str) 控制模型的推理强度
    // 允许的值有：
    // - "low"
    // - "medium"
    // - "high"
    // - "xhigh"
    // - "max"
    // - null
    "reasoning_effort": null,

    // (bool) 删除上下文里的推理内容
    // 大部分 API 会拒绝我们回传推理内容
    // 你可以设置为 false 来关闭此功能
    // 但某些 API 可能会因此调用失败
    "remove_reasoning_prompt": null,

    // (str) Request Statistics Message 模板
    // 用于生成一段自定义的统计文本
    "request_statistics_template": null,

    // (str) 渲染风格
    // 用于指定文本转图片时的CSS样式文件
    "render_style": null,

    // (str) 渲染 HTML 模板
    // 用于指定文本转图片时的HTML模板文件
    "render_html_template": null,

    // (str) 渲染 HTML 标题
    // 用于指定文本转图片时的图片标题
    "render_title": null,

    // (str) 渲染尾部注释
    // 在生成图片的最下方添加一小段独立文本
    "render_document_bottom_comment": null,

    // (bool) 是否加载提示词
    // 此选项会被API接口中传入的 load_prompt 参数覆盖
    "load_prompt": null,

    // (bool) 是否保存上下文
    // 此选项会被API接口中传入的 save_context 参数覆盖
    "save_context": null,

    // (bool) 是否只保存新消息
    // 如果启用，则只保存新消息，而不是追加到历史消息中
    "save_new_only": null,

    // (bool) 是否在保存时丢弃非文本数据
    "save_text_only": null,

    // (str) 用户名
    // 这个值在模板中为 `user_custom_name`
    "user_name": null,

    // (str) 用户资料
    // 如果提示词中含有{{user_profile}}变量
    // 将会展开为该值
    "user_profile": null,

    // (int | float) 用户自定义年龄
    // 这个值在模板中为 `user_custom_age`
    "user_age": null,

    // (str) 用户性别
    // 这个值在模板中为 `user_custom_gender`
    "user_gender": null,
    
    // (str) 时区设置
    // 用于控制模板展开器中的时间变量
    "timezone": null,

    // (bool) 是否允许跨用户数据访问
    // 如果为true, 则使用请求里指定的的用户进行加载和保存
    // 如果为false, 则只能对当前用户操作
    // 如果为null, 则继承全局配置
    // 如果要访问的目标用户也设置了该值
    // 且对方该值为false, 则请求将会自动回退到当前用户的上下文中
    "cross_user_data_access": null,

    // (bool) 是否忽略新请求中的非文本数据
    "new_requests_text_only": null,

    // (bool) 是否允许工具调用
    "allow_tool_calls": null,

    // (dict[str, Any]) 用户附加配置数据
    // 用于存储某些与用户相关的数据
    // 其键应该是 Client 自己的专属ID
    // 键值可以是任何数据类型
    "additional_user_data": {}
}
```
当配置值为null时，将使用其对应的全局配置值。