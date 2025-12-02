# @复读机Repeater
**- Only Chat, Focus Chat. -**

*注：本仓库仅为后端实现，NoneBot插件部分请查看[`Repater-Nonebot-Plugin`](https://github.com/qeggs-dev/repeater-qq-ai-chatbot-nonebot-plugins)*

一个基于[`NoneBot`](https://nonebot.dev/)和[`OpenAI SDK`](https://pypi.org/project/openai/)开发的**实验性**QQ聊天机器人
**此仓库仅为后端实现，NoneBot插件部分请查看[`Repater-Nonebot-Plugin`](https://github.com/qeggs-dev/repeater-qq-ai-chatbot-nonebot-plugins)**
将原始会话数据的处理直接公开给用户使用
接近直接操作API的灵活度体验

与其他QQ机器人相比，复读机具有以下特点：

 - 平行数据管理：支持平行数据管理，用户可以随意切换平行数据，而不需要担心数据丢失。
 - 多模型支持：支持OpenAI接口的模型即可调用，可以根据需要选择不同的模型进行对话。
 - 超高自由度：用户可以自定义会话注入、切换、删除，以及自定义提示词
 - MD图片渲染：可以将回复以图片的形式渲染发送，降低其妨碍用户正常聊天的程度（但鬼知道为什么这东西竟然不支持Emoji渲染！！！）
 - 命令别名触发：不管是缩写还是全文，都可以触发命令操作
 - 用户自治设计：用户可以自己管理自己的所有用户数据
 - 多预设人设：复读机支持多预设人设，用户可以自由选择自己喜欢的人设进行对话
> 注：拟人化并非复读机的赛道，复读机不对拟人化需求做过多保证，如有需要请自行引导或编写提示词。

## 注意事项:
 - 本服务由一位 `16岁自学开发者`(现在17了) 使用AI协作开发，公益项目，如果你愿意捐赠，可以在机器人的**QQ空间**中找到赞赏码以支持项目运营(或是支持开发者)。
 - 使用者需确认生成内容的合法性，并自行承担使用本服务可能产生的风险。
 - 如果你觉得这个Bot非常好用，请去看一下[`Deepseek`](https://www.deepseek.com/)的官网吧，这个Bot最初就是基于他们的模型API文档开发的。

---

## License
这个项目基于[MIT License](LICENSE)发布。

---

### 依赖项:
| Name              | Version  | License                              | License Link                                                                        | Where it is used                   | Reasons                               |
|-------------------|----------|--------------------------------------|-------------------------------------------------------------------------------------|------------------------------------|---------------------------------------|
| Markdown          | 3.8.2    | BSD 3-Clause License                 | [BSD-3-Clause](https://github.com/Python-Markdown/markdown/blob/master/LICENSE.md)  | `Markdown`                         | Parses Markdown text into HTML        |
| pyyaml            | 6.0.2    | MIT License                          | [MIT](https://github.com/yaml/pyyaml/blob/main/LICENSE)                             | `API` & `ConfigManager`            | Read configuration file               |
| aiofiles          | 24.1.0   | Apache Software License              | [Apache-2.0](https://github.com/Tinche/aiofiles/blob/main/LICENSE)                  | `core.DataManager`                 | Asynchronous file support             |
| environs          | 14.2.0   | MIT License                          | [MIT](https://github.com/sloria/environs/blob/main/LICENSE)                         | `run_fastapi.py` & `ConfigManager` | Support for environment variables     |
| fastapi           | 0.115.13 | MIT License                          | [MIT](https://github.com/fastapi/fastapi/blob/master/LICENSE)                       | `API`                              | Build API                             |
| httpx             | 0.28.1   | BSD License                          | [BSD-3-Clause](https://github.com/encode/httpx/blob/master/LICENSE.md)              | `core.FuncerClient`                | Asynchronous HTTP client              |
| imgkit            | 1.2.3    | MIT License                          | [MIT](https://github.com/jarrekk/imgkit/blob/master/LICENSE)                        | `Markdown`                         | Render HTML as an image               |
| loguru            | 0.7.3    | MIT License                          | [MIT](https://github.com/Delgan/loguru/blob/master/LICENSE)                         | *Entire Project*                   | Logging                               |
| openai            | 1.90.0   | Apache Software License              | [Apache-2.0](https://github.com/openai/openai-python/blob/main/LICENSE)             | `core.CallAPI`                     | Call the OpenAI API                   |
| orjson            | 3.10.18  | Apache Software License; MIT License | [Apache-2.0](https://github.com/ijl/orjson/blob/master/LICENSE-APACHE) / [MIT](https://github.com/ijl/orjson/blob/master/LICENSE-MIT) | `core.DataManager` | High-performance JSON  resolution |
| pydantic          | 2.11.7   | MIT License                          | [MIT](https://github.com/pydantic/pydantic/blob/main/LICENSE)                       | `core.ConfigManager` & `API`       | Simple and convenient data validation |
| python-multipart  | 0.0.20   | Apache Software License              | [Apache-2.0](https://github.com/Kludex/python-multipart/blob/master/LICENSE.txt)    | `core.DataManager` & `API`         | Support for form data                 |
| uvicorn           | 0.34.3   | BSD License                          | [BSD-3-Clause](https://github.com/Kludex/uvicorn/blob/main/LICENSE.md)              | `run_fastapi.py`                   | Run FastAPI                           |
| numpy             | 2.3.4    | BSD License                          | [BSD-3-Clause](https://github.com/numpy/numpy/blob/main/LICENSE.txt)                | *Entire Project*                   | Speed up batch computing of data      |
| python-box        | 7.3.2    | MIT License                          | [MIT](https://github.com/cdgriffith/Box/blob/master/LICENSE)                        | `core.Global_Config_Manager`       | Mixed configuration files             |

---

## 安装部署

**推荐Python3.11以上版本安装**
> PS: 复读机可能会兼容Python3.11以前的版本
> 但我们并未对其进行过测试
> 此处3.11为开发环境版本

### 自动安装

1. 将项目克隆到本地
2. 进入项目目录
5. 运行`run.py`启动器 (详情请查看[Sloves_Starter](https://github.com/qeggs-dev/Sloves_Starter))

### 手动安装

1. 将项目克隆到本地
2. 进入项目目录
3. 执行`python3 -m venv .venv`创建虚拟环境
4. 执行`.venv/bin/activate`激活虚拟环境(Windows下则是`.venv\Scripts\activate`)
5. 执行`pip install -r requirements.txt`安装依赖
6. 执行`python3 run_fastapi.py`启动服务

PS: `run.py`启动器会在完成所有操作后启动主程序，而这只需要你保证你的配置正确
并且每一次你都可以通过启动器来启动程序

---

## 环境变量表

| 环境变量 | 描述 | 是否必填 | 默认值(*示例值*) |
| :---: | :---: | :---: | :---: |
| `*API_KEY` | API_Key (具体变量名由`API_INFO.API_FILE_PATH`指向 文件中`ApiKeyEnv`字段的名称) | **必填** | *\*可从[Deepseek开放平台/API Keys](https://platform.deepseek.com/api_keys)页面获取* |
| `ADMIN_API_KEY` | 管理员API_Key (用于框架的管理员操作身份验证) | **选填但生产环境建议填写** | *\*自动生成随机 API Key* |
| `CONFIG_DIR` | 配置文件夹路径 | **选填** | `./config/project_config` |
| `CONFIG_FORCE_LOAD_LIST` | 配置文件强制加载列表(元素为配置文件路径) | **选填** | *`["./config/project_config/configs.json", "./config/project_config/configs2.json"]`* |
| `CONFIG_ENVIRONMENT` | 配置文件环境 | **选填** | `DEV` |
| `HOST` | 服务监听的IP | **选填** | `0.0.0.0` |
| `PORT` | 服务监听的端口 | **选填** | `8080` |
| `WORKERS` | 服务监听的进程数 | **选填** | `1` |
| `RELOAD` | 是否自动重启 | **选填** | `false` |

## 配置文件

**默认值：**
```json
{
    "api_info": {
        "api_file_path": "./config/api_info.json",
        "default_model_uid": "chat"
    },
    "blacklist": {
        "file_path": "./config/blacklist.regex",
        "match_timeout": 10
    },
    "bot_info": {
        "name": "Repeater",
        "birthday": {
            "day": 28,
            "month": 6,
            "year": 2024
        }
    },
    "callapi": {
        "max_concurrency": 1000
    },
    "context": {
        "auto_shrink_length": null
    },
    "core": {
        "version": ""
    },
    "logger": {
        "file_path": "./logs/repeater-log-{time:YYYY-MM-DD_HH-mm-ss.SSS}.log",
        "level": "INFO",
        "rotation": "10 MB",
        "retention": "7 days",
        "compression": "zip"
    },
    "model": {
        "default_model_uid": "chat",
        "default_temperature": 1.0,
        "default_top_p": 1.0,
        "default_max_tokens": 4096,
        "default_max_completion_tokens": 4096,
        "default_frequency_penalty": 0.0,
        "default_presence_penalty": 0.0,
        "default_stop": [],
        "stream": true
    },
    "prompt": {
        "dir": "./config/prompt/presets",
        "suffix": ".md",
        "encoding": "utf-8",
        "preset_name": "default"
    },
    "render": {
        "default_image_timeout": 60.0,
        "markdown": {
            "to_image": {
                "default_style": "light",
                "styles_dir": "./config/styles",
                "style_file_encoding": "utf-8",
                "preprocess_map": {
                    "before": {},
                    "after": {}
                },
                "wkhtmltoimage_path": "wkhtmltoimage",
                "output_dir": "./workspace/temp/render"
            }
        }
    },
    "request_log": {
        "dir": "./workspace/request_log",
        "auto_save": true,
        "debonce_save_wait_time": 1200.0,
        "max_cache_size": 1000
    },
    "server": { // 这里的几个字段为null或不填则会使用环境变量中定义的配置
        "host": null,
        "port": null,
        "workers": null,
        "reload": null
    },
    "static": {
        "readme_file_path": "./README.md",
        "static_dir": "./static"
    },
    "time": {
        "time_offset": 0.0
    },
    "user_config_cache": {
        "downgrade_wait_time": 600.0,
        "debounce_save_wait_time": 1000.0
    },
    "user_data": {
        "dir": "./workspace/data/user_data",
        "branches_dir_name": "branches",
        "metadata_file_name": "metadata.json",
        "cache_medadata": false,
        "cache_data": false
    },
    "user_nickname_mapping": {
        "file_path": "./config/user_nickname_mapping.json"
    },
    "web": {
        "index_web_file": "./static/index.html"
    }
}
```

PS: 配置读取时键名不区分大小写，但建议使用小写格式
配置管理器会扫描环境变量`CONFIG_DIR`下的所有json/yaml文件
并按照路径名顺序排列，后加载配置中的字段会覆盖之前的配置
你也可以使用环境变量`CONFIG_FORCE_LOAD_LIST`来强制按照指定的顺序加载配置

---

## 各种配置文件的数据格式

1. 配置文件格式：
参考[配置文件](#配置文件)

2. api_info文件格式：
```json
[
    {
        "name": "Deepseek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "url": "https://api.deepseek.com",
        "models": [
            {
                "name": "Deepseek Think Model",
                "id": "deepseek-reasoner",
                "uid": "deepseek-reasoner",
                "type": "chat"
            },
            {
                "name": "Deepseek Chat Model",
                "id": "deepseek-chat",
                "uid": "deepseek-chat",
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
                "type": "chat"
            }
        ]
    }
]
```
YAML同理
PS: 目前仅支持LLM Chat的任务类型(系统不会检查该字段，但APIINFO模块会收集相关组)
models中定义该模型的url时会覆盖上层的url
支持兼容OpenAI接口的Chat.Completion模型

3. blacklist.regex (或其他任何RegexChecker处理的文件格式)文件:
```re
[REGEX PARALLEL FILE]
.*example.*
```
PS: 首行必须是`[REGEX PARALLEL FILE]`或`[REGEX SERIES FILE]`，表示该文件是`并行`还是`串行`匹配
之后每行都是`正则表达式`，匹配到的`昵称`或`user_id`的请求将会被**拒绝**

4. UserNicknameMapping.json 文件格式：
```json
{
    "old_nickname": "new_nickname",
    "user_id": "new_nickname"
}
```
`原始昵称`到`模型看到的昵称`的映射关系
键可以是`昵称`或`user_id`，值是`新的昵称`

---

## Markdown图片渲染样式

| 风格 | 译名 |
| :---: | :---: |
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

---

## 人格预设

| 预设 | 描述 |
| :---: | :---: |
| `default` | 默认 |
| `sister` | 姐姐 |
| `english` | 英语 |
| `japanese` | 日语 |
| `french` | 法语 |
| `russian` | 俄语 |
| `arabic` | 阿拉伯语 |
| `spanish` | 西班牙语 |

(求翻译，我只会中文一个语言)

---

## 模板展开系统

### 变量表

| 变量 | 描述 | 参数 |
| :---: | :---: | :---: |
| `user_id` | 用户ID | 无 |
| `user_name` | 用户名 | 无 |
| `nickname` | 昵称 | 无 |
| `botname` | Bot名称 | 无 |
| `user_age` | 用户年龄 | 无 |
| `user_gender` | 用户性别 | 无 |
| `user_info` | 用户信息 | 无 |
| `birthday` | 生日 | 无 |
| `BirthdayCountdown` | 生日倒计时 | 无 |
| `model_uid` | 模型类型 | 无 |
| `zodiac` | Bot星座 | 无 |
| `time` | 当前时间 | 无 |
| `age` | Bot年龄 | 无 |
| `random` | 随机数 | 随机数下限，随机数上下限 |
| `randfloat` | 随机浮点数 | 随机数下限，随机数上下限 |
| `randchoice` | 随机选择 | 抽取内容 |
| `generate_uuid` | 生成UUID | 无 |
| `copytext` | 重复文本 | 重复文本， 重复次数, 间隔符 |
| `text_matrix` | 文本矩阵 | 重复文本，列数，行数，间隔符，换行符 |
| `random_matrix` | 0~1随机矩阵 | 矩阵行数，矩阵列数 |

### 变量传参方式

优先使用shell格式分割，失败时再按空格分割
```Plaintext
{random 1 10}
{randchoice a b c d e}
{copytext a 5 " "}
{text_matrix a 5 5 " " "<esc:"\n">"}
```

### 转义序列

```Plaintext
转义处理器：<esc:"">
<esc:"\0">空字符
<esc:"\n">换行符
<esc:"\r">回车符
<esc:"\t">制表符
<esc:"\a">响铃符
<esc:"\b">退格符
<esc:"\f">换页符
<esc:"\v">垂直制表符
<esc:"\e">转义符
<esc:"\xhh">二位16进制字符
<esc:"\uHHHH">四位16进制字符
<esc:"\UHHHHHHHH">八位16进制字符
<esc:"\oOOO">8进制字符
<esc:"\dDDD">10进制字符
```
PS: 转义必须保证转义处理器一字不漏，否则会以普通文本输出
引号必须存在，它和其他部分共同组成转义序列的边界

---

## 接口表

| 请求 | URL | 参数类型 | 参数(*可选*) | 描述 | 响应类型 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| `GET` | `/` | 无 | 无 | 获取Index Web | `Web页面` |
| `GET` | `/index.html` | 无 | 无 | (同上) 获取Index Web | `Web页面` |
| `GET` | `/docs` | 无 | 无 | 获取接口文档 | `Web页面` |
| `POST` | `/chat/completion/{user_id:str}` | JSON请求体 | *`message(str)`*<br/>*`user_name(str)`*<br/>*`role(str) = 'user'`*<br/>*`role_name(str)`*<br/>*`model_uid(str)`*<br/>*`load_prompt(bool) = true`*<br/>*`save_context(bool) = true`*<br/>*`reference_context_id(str)`*<br/>*`continue_completion(bool)`*  | AI聊天 | `JSON响应对象` 或 `流式Delta对象` |
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
| `PUT` | `/userdata/config/set/{user_id:str}/{value_type:str}` | 表单 | `key(str)`<br/>`value(Any)` | 设置配置 | `JSON对象` |
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
| `POST` | `/admin/regenerate/admin_key` | 请求头 | `X-Admin-API-Key(str)` | 重新生成管理密钥 | `JSON对象` |

---

## 用户配置表

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `parset_prompt_name` | `str` | 项目配置中`PROMPT.PARSET_NAME`的值 | 在启动时如果没有检查到自定义提示词，默认选择的预设提示词文件名(此处没有文件后缀，如`default`，实际文件名中会与`PROMPT.DEFAULT_SUFFIX`拼接) |
| `model_uid` | `str` | 项目配置中`MODEL.DEFAULT_MODEL_UID`的值 | 模型UID |
| `temperature` | `float` | 项目配置中`MODEL.DEFAULT_TEMPERATURE`的值 | 模型温度 |
| `top_p` | `float` | 项目配置中`MODEL.DEFAULT_TOP_P`的值 | 模型top_p |
| `max_tokens` | `int` | 项目配置中`MODEL.DEFAULT_MAX_TOKENS`的值 | 模型最大生成长度(OpenAI计划丢弃此参数，但为了兼容性，此处仍然保留) |
| `max_completion_tokens` | `int` | 项目配置中`MODEL.DEFAULT_MAX_COMPLETION_TOKENS`的值 | 模型最大补全长度 |
| `stop` | `list[str]` | 项目配置中`MODEL.DEFAULT_STOP`的值 | 模型停止词 |
| `frequency_penalty` | `float` | 项目配置中`MODEL.DEFAULT_FREQUENCY_PENALTY`的值 | 模型频率惩罚 |
| `presence_penalty` | `float` | 项目配置中`MODEL.DEFAULT_PRESENCE_PENALTY`的值 | 模型存在性惩罚 |
| `auto_shrink_length` | `int` | 项目配置中`MODEL.AUTO_SHRINK_LENGTH`的值 | 自动上下文长度限制的最大值(为0时不自动限制长度) |

---

## 命令表：

\*已被移动至[Repeater NoneBot插件仓库](https://github.com/qeggs-dev/repeater-qq-ai-chatbot-nonebot-plugins)

---

## 相关仓库

[Sloves_Starter](https://github.com/qeggs-dev/Sloves_Starter)