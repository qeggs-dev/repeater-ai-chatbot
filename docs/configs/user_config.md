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
    // (str) 时区设置
    // 用于控制模板展开器中的{time}变量
    "timezone": null,
    
    // (str) 预设提示词
    // 用于快速路由定义好的提示词文件
    "parset_prompt_name": null,

    // (str) 模型UID
    // 用于指定消息处理模型
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

    // (str) 渲染风格
    // 用于指定文本转图片时的CSS样式文件
    "render_style": null,

    // (str) 渲染HTML模板
    // 用于指定文本转图片时的HTML模板文件
    "render_html_template": null,

    // (str) 渲染HTML标题
    // 用于指定文本转图片时的图片标题
    "render_title": null,

    // (bool) 是否加载提示词
    // 此选项会被API接口中传入的 load_prompt 参数覆盖
    "load_prompt": null,

    // (bool) 是否保存上下文
    // 此选项会被API接口中传入的 save_context 参数覆盖
    "save_context": null,

    // (str) 用户资料
    // 如果提示词中含有{user_profile}变量
    // 将会展开为该值
    "user_profile": null,

    // (bool) 是否在保存时丢弃非文本数据
    "save_text_only": null,

    // (bool) 是否只保存新消息
    // 如果启用，则只保存新消息，而不是追加到历史消息中
    "save_new_only": null,

    // (bool) 是否允许跨用户数据访问
    // 如果为true, 则使用请求里指定的的用户进行加载和保存
    // 如果为false, 则只能对当前用户操作
    // 如果为null, 则继承全局配置
    "cross_user_data_access": null,

    // (dict[str, Any]) 用户附加配置数据
    // 用于存储某些与用户相关的数据
    // 其键应该是 Client 自己的专属ID
    // 键值可以是任何数据类型
    "additional_user_data": {}
}
```
当配置值为null时，将使用其对应的全局配置值。