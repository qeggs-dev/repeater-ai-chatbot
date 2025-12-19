# Repeater API 接口表

| 请求 | URL | 参数类型 | 参数(*可选*) | 描述 | 正常响应类型 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| `GET` | `/` | 无 | 无 | 获取Index Web | `Web页面` |
| `GET` | `/index.html` | 无 | 无 | (同上) 获取Index Web | `Web页面` |
| `GET` | `/docs` | 无 | 无 | 获取接口文档 | `Web页面` |
| `POST` | `/chat/completion/{user_id:str}` | JSON请求体 | *`message(str)`*<br/>*`user_info.username(str)`*<br/>*`user_info.nickname(str)`*<br/>*`user_info.age(int)`*</br>*`user_info.gender(str)`*<br/>*`role(str)`*<br/>*`role_name(str)`*<br/>*`model_uid(str)`*<br/>*`load_prompt(bool)`*<br/>*`save_context(bool)`*<br/>*`image_url(str\|list[str])`*<br/>*`reference_context_id(str)`*<br/>*`continue_completion(bool)`*<br/>*`stream(bool)`*  | AI聊天 | `JSON响应对象` 或 `流式Delta对象` |
| `POST` | `/render/{user_id:str}`| JSON请求体 | **`text(str)`**<br/>*`style(str)`*<br/>*`timeout(float)`* | 文本渲染 | `JSON对象` |
| `POST` | `/userdata/variable/expand/{user_id:str}` | JSON请求体 | *`username(str)`*<br/>`text(str)` | 变量解析 | `JSON对象` |
| `GET` | `/userdata/context/get/{user_id:str}` | | | 获取上下文 | `JSON列表` |
| `GET` | `/userdata/context/length/{user_id:str}` | | | 获取上下文长度 | `JSON对象` |
| `GET` | `/userdata/context/userlist` | | | 获取用户列表 | `JSON列表` |
| `POST` | `/userdata/context/withdraw/{user_id:str}` | 表单 | `context_pair_num(int)` | 撤回上下文(按照上下文对) | `JSON对象` |
| `POST` | `/userdata/context/inject/{user_id:str}` | JSON请求体 | `user_content(str)`<br/>`assistant_content(str)` | 注入上下文 | `JSON对象` |
| `POST` | `/userdata/context/rewrite/{user_id:str}` | 表单 | `index(int)`<br/>`content(str)`<br/>*`reasoning_content(str)`* | 重写上下文 | `JSON列表` |
| `GET` | `/userdata/context/branchs/{user_id:str}` | | | 获取用户分支ID列表 | `JSON列表` |
| `GET` | `/userdata/context/now_branch/{user_id:str}` | | | 获取用户当前分支ID | `纯文本` |
| `PUT` | `/userdata/context/change/{user_id:str}` | 表单 | `new_branch_id(str)` | 切换上下文 | `纯文本` |
| `DELETE` | `/userdata/context/delete/{user_id:str}` | | | 删除上下文 | `纯文本` |
| `GET` | `/userdata/prompt/get/{user_id:str}` | | | 获取提示词 | `纯文本` |
| `PUT` | `/userdata/prompt/set/{user_id:str}` | 表单 | `prompt(str)` | 设置提示词 | `纯文本` |
| `GET` | `/userdata/prompt/userlist` | | | 获取用户列表 | `JSON列表` |
| `GET` | `/userdata/prompt/branchs/{user_id:str}` | | | 获取用户分支ID列表 | `JSON列表` |
| `GET` | `/userdata/prompt/now_branch/{user_id:str}` | | | 获取用户当前分支ID | `纯文本` |
| `PUT` | `/userdata/prompt/change/{user_id:str}` | 表单 | `new_branch_id(str)` | 切换提示词 | `纯文本` |
| `DELETE` | `/userdata/prompt/delete/{user_id:str}` | | | 删除提示词 | `纯文本` |
| `GET` | `/userdata/config/get/{user_id:str}` | | | 获取配置 | `JSON对象` |
| `PUT` | `/userdata/config/set/{user_id:str}/{key:str}` | 表单 | `type(str)`<br/>`value(Any)` | 设置配置 | `JSON对象` |
| `PUT` | `/userdata/config/set/{user_id:str}` | 表单 | `config(JSON对象)` | 批量配置设置 | `JSON对象` |
| `PUT` | `/userdata/config/delkey/{user_id:str}` | 表单 | `key(str)` | 删除配置 | `JSON对象` |
| `GET` | `/userdata/config/userlist` | | | 获取用户列表 | `JSON列表` |
| `GET` | `/userdata/config/branchs/{user_id:str}` | | | 获取用户分支ID列表 | `JSON列表` |
| `GET` | `/userdata/config/now_branch/{user_id:str}` | | | 获取用户当前分支ID | `纯文本` |
| `PUT` | `/userdata/config/change/{user_id:str}` | 表单 | `new_branch_id(str)` | 切换分支数据 | `纯文本` |
| `DELETE` | `/userdata/config/delete/{user_id:str}` | | | 删除用户配置文件 | `纯文本` |
| `GET` | `/userdata/file/{user_id:str}.zip` | | | 获取用户数据 | `ZIP文件` |
| `GET` | `/request_log` | | | 获取调用日志(不推荐) | `JSON列表` |
| `GET` | `/request_log/list` | | | 获取调用日志(同上) | `JSON列表` |
| `GET` | `/request_log/stream` | | | 流式获取调用日志(推荐) | `JSONL流` |
| `GET` | `/file/render/{file_uuid:str}.png` | | | 获取图片渲染输出文件 | `PNG图片` |
| `POST` | `/admin/reload/apiinfo` | 请求头 | `X-Admin-API-Key(str)` | 刷新API信息 | `JSON对象` |
| `POST` | `/admin/regenerate/admin_key` | 请求头 | `X-Admin-API-Key(str)` | 重新生成管理密钥 | `JSON对象` |
| `POST` | `/admin/configs/reload` | 请求头 | `X-Admin-API-Key(str)` | 重新加载配置 (警告：某些模块会缓存配置结果，这可能导致模块之间的配置差异！) | `JSON对象` |
| `POST` | `/admin/configs/{name:str}/seek/{index:int}` | 请求头 | `X-Admin-API-Key(str)` | 移动指针在指定配置栈中的位置 | `JSON对象` |
| `GET` | `/version` | | | 获取版本信息 | `JSON对象` |
| `GET` | `/version/api` | | | 获取API版本信息 | `纯文本` |
| `GET` | `/version/core` | | | 获取核心版本信息 | `纯文本` |