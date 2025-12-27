# Chat API

负责与 AI 进行对话
服务器会自动管理对话状态文件

- **`/chat/completion/{user_id:str}`**
  - **Requset**
    - **method:** `POST`
    - **type:** `JSON`
    - **Request Body**:
      - `message(str)` 用户发送的消息，允许为空，但这时模型的行为可能是未定义的
      - `user_info` 用户信息，全部可选
        - `username(str)` 用户名
        - `nickname(str)` 昵称
        - `age(int | float)` 年龄
        - `gender(str)` 性别
      - `role(str)` 用户角色，可选值：`user`、`assistant`、`system`，默认为 `user`
      - `role_name(str)` 用户角色名称，用于模型区分相同上下文里相同用户角色的不同的用户
      - `model_uid(str)` 模型UID，用于临时指定一个模型对话，如果不填则根据配置系统推断值
      - `load_prompt(bool)` 是否加载Prompt，如果不填则根据配置系统推断值
      - `save_context(bool)` 是否在完成后保存上下文，如果不填则根据配置系统推断值
      - `image_url(str | list[str])` 图片URL，用于视觉输入，支持单张或多张图片，需要保证链接**长期有效**或使用 `base64` ，以及确保模型可以正确处理视觉输入
      - `reference_context_id(str)` 从指定的 `user_id` 获取上下文，如果指定了该项，则不会从 `user_id` 获取上下文，但是保存仍然指向 `user_id`
      - `stream(bool)` 是否流式返回（设置该值为 `true` 需要保证在配置中启用了流式处理器，否则会返回`503`错误码）
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `reasoning_content(str)` CoT回复内容，即使模型没有返回CoT它仍然存在，注意判断逻辑应为非null和非空字符串
      - `content(str)` AI回复内容
      - `user_raw_input(str)` 用户发送的原始消息
      - `user_input(str | list[ContentBlock])` 用户发送的消息经过格式化后处理后的内容，使用[OpenAI Chat Completion User Message Content](https://platform.openai.com/docs/api-reference/chat/create#chat_create-messages-user_message-content)格式
      - `model_group(str)` 模型组，由[API_Info文件](../configs/api_info.md)决定
      - `model_name(str)` 模型名称，通常是该模型的可读名称
      - `model_type(str)` 模型类型, 由[API_Info文件](../configs/api_info.md)决定，通常这个接口返回的是`chat`
      - `create_time(int)` 提交请求到API时API厂商报告的请求创建时间戳
      - `id(str)` 请求ID，通常是一个随机的字符串，由API厂商生成，通常可以被作为唯一标识使用
      - `finish_reason_code(str)` 模型结束生成的原因，由API厂商提供
      - `finish_reason_cause(str)` 模型结束生成的原因，该字段为可读版本，由程序自动生成
      - `status(int)` 状态码，这里和http状态码一致，只是为了报告而写，通常你应该优先选择检查http报告的状态码而不是这个字段

注：该API有**RUL(Request User Lock)**
在 `user_id` 相同且上一个请求**未完成**时
该API将会**堵塞**后来的请求
直到该用户的上一个请求完成
这保证了用户在频繁发起请求时数据的线性处理
`user_id` 不同时RUL不会阻碍它们并行处理

由于程序是 Async 架构的
初始化阶段是计算密集型任务居多
大概持续 `40ms` 左右
在这段时间内，当前执行的协程会无法让出执行权
所以还请注意