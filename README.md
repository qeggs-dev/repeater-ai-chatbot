# @复读机Repeater
**- Only Chat, Focus Chat. -**

一个主要基于[`OpenAI SDK`](https://pypi.org/project/openai/)开发的聊天机器人
将原始会话数据的处理直接公开给用户使用
以达到接近直接操作API的灵活度体验

目前，复读机具有以下特点：

 - 平行数据管理：支持平行数据管理，用户可以随意切换平行数据，减少数据丢失的风险
 - 多模型支持：支持OpenAI接口的对话模型即可调用，可以根据需要选择不同的模型进行对话
 - 超高自由度：用户可以自定义会话注入、切换、删除，以及自定义提示词和模型参数
 - MD图片渲染：可以将回复以图片的形式渲染发送，减少对正常聊天的干扰
 - 用户自治设计：用户可以自己管理自己的所有用户数据
 - 多预设人设：复读机支持多预设人设，用户可以自由选择自己喜欢的人设进行对话

注：拟人化并非复读机的赛道，复读机不对拟人化需求做过多保证，如有需要请自行引导或编写提示词。

---

## 注意事项:
 - 使用者需确认生成内容的合法性，并自行承担使用本服务可能产生的风险。
 - 如果你觉得这个Bot非常好用，请去看一下[`Deepseek`](https://www.deepseek.com/)的官网吧，这个Bot最初就是基于他们的模型API文档开发的。
 - 机器人本体是免费的，但开发者不承担使用时的API费用，还请注意。

---

## License
这个项目基于[MIT License](LICENSE)发布。

---

### 依赖项:
| Name              | Version  | License                              | License Link                                                                        | Where it is used                    | Reasons                               |
|-------------------|----------|--------------------------------------|-------------------------------------------------------------------------------------|-------------------------------------|---------------------------------------|
| Markdown          | 3.8.2    | BSD 3-Clause License                 | [BSD-3-Clause](https://github.com/Python-Markdown/markdown/blob/master/LICENSE.md)  | `Markdown`                          | Parses Markdown text into HTML        |
| pyyaml            | 6.0.2    | MIT License                          | [MIT](https://github.com/yaml/pyyaml/blob/main/LICENSE)                             | `API` & `ConfigManager`             | Read configuration file               |
| aiofiles          | 24.1.0   | Apache Software License              | [Apache-2.0](https://github.com/Tinche/aiofiles/blob/main/LICENSE)                  | `core.DataManager`                  | Asynchronous file support             |
| environs          | 14.2.0   | MIT License                          | [MIT](https://github.com/sloria/environs/blob/main/LICENSE)                         | `run_repeater.py` & `ConfigManager` | Support for environment variables     |
| fastapi           | 0.115.13 | MIT License                          | [MIT](https://github.com/fastapi/fastapi/blob/master/LICENSE)                       | `API`                               | Build API                             |
| httpx             | 0.28.1   | BSD License                          | [BSD-3-Clause](https://github.com/encode/httpx/blob/master/LICENSE.md)              | `core.FuncerClient`                 | Asynchronous HTTP client              |
| playwright        | 1.56.0   | Apache-2.0                           | [Apache-2.0](https://github.com/microsoft/playwright-python/blob/main/LICENSE)      | `Markdown_Render`                   | Render HTML as an image               |
| loguru            | 0.7.3    | MIT License                          | [MIT](https://github.com/Delgan/loguru/blob/master/LICENSE)                         | *Entire Project*                    | Logging                               |
| openai            | 1.90.0   | Apache Software License              | [Apache-2.0](https://github.com/openai/openai-python/blob/main/LICENSE)             | `core.CallAPI`                      | Call the OpenAI API                   |
| orjson            | 3.10.18  | Apache Software License; MIT License | [Apache-2.0](https://github.com/ijl/orjson/blob/master/LICENSE-APACHE) / [MIT](https://github.com/ijl/orjson/blob/master/LICENSE-MIT) | `core.DataManager` | High-performance JSON  resolution |
| pydantic          | 2.11.7   | MIT License                          | [MIT](https://github.com/pydantic/pydantic/blob/main/LICENSE)                       | `core.ConfigManager` & `API`        | Simple and convenient data validation |
| python-multipart  | 0.0.20   | Apache Software License              | [Apache-2.0](https://github.com/Kludex/python-multipart/blob/master/LICENSE.txt)    | `core.DataManager` & `API`          | Support for form data                 |
| uvicorn           | 0.34.3   | BSD License                          | [BSD-3-Clause](https://github.com/Kludex/uvicorn/blob/main/LICENSE.md)              | `run_repeater.py`                   | Run FastAPI                           |
| numpy             | 2.3.4    | BSD License                          | [BSD-3-Clause](https://github.com/numpy/numpy/blob/main/LICENSE.txt)                | *Entire Project*                    | Speed up batch computing of data      |
| python-box        | 7.3.2    | MIT License                          | [MIT](https://github.com/cdgriffith/Box/blob/master/LICENSE)                        | `core.Global_Config_Manager`        | Mixed configuration files             |
| tzdata            | 2025.2   | Apache Software License              | [Apache-2.0](https://github.com/python/tzdata/blob/master/LICENSE)                  | `core.Text_Template_Processer`      | Get timezone information              |

---

## 安装部署

**推荐Python3.11及以上版本安装**
> PS: 复读机可能会兼容Python3.11以前的版本
> 但我们并未对其进行过测试
> 复读机有可能会需要至少3.10的版本
> 此处3.11为开发环境版本

### 自动安装

1. 将项目克隆到本地
2. 进入项目目录
5. 运行`run.py`启动器 (该项目的详情请查看[Sloves_Starter](https://github.com/qeggs-dev/Sloves_Starter))

### 手动安装

1. 将项目克隆到本地
2. 进入项目目录
3. 执行`python3 -m venv .venv`创建虚拟环境
4. 执行`.venv/bin/activate`激活虚拟环境(Windows下则是`.venv\Scripts\activate`)
5. 执行`pip install -r requirements.txt`安装依赖
6. 执行`python3 run_repeater.py`启动服务

PS: `run.py`启动器会在完成所有操作后启动主程序，而这只需要你保证你的配置正确
并且每一次你都可以通过启动器来启动程序

---

## 跨平台

本项目并未在项目中加入平台强相关逻辑
经过测试，Repeater可以在 Windows、Linux 上正常运行
启动器也根据平台特性做了适配
暂未测试过 MacOS (因为没钱买苹果)

---

## 环境变量表

| 环境变量 | 描述 | 是否必填 | 默认值(*示例值*) |
| :---: | :---: | :---: | :---: |
| `*API_KEY` | API_Key (具体变量名由`API_INFO.API_FILE_PATH`指向 文件中`ApiKeyEnv`字段的名称) | **必填** | 从你所使用的AI厂商开放平台获取 API Key |
| `ADMIN_API_KEY` | 管理员API_Key (用于Repeater的管理员操作身份验证) | **选填但生产环境建议填写</br>如果填写的不够随机，程序会报错</br>建议先执行一次取生成的API_Key** | *\*自动生成随机 API Key* |
| `CONFIG_DIR` | 配置文件夹路径 | **选填** | `./config/project_config` |
| `CONFIG_FORCE_LOAD_LIST` | 配置文件强制加载列表(元素为配置文件路径) | **选填** | *`["./config/project_config/configs.json", "./config/project_config/configs2.json"]`* |
| `HOST` | 服务监听的IP | **选填** | `0.0.0.0` |
| `PORT` | 服务监听的端口 | **选填** | `8080` |
| `WORKERS` | 服务监听的进程数 | **选填** | `1` |
| `RELOAD` | 是否自动重启 | **选填** | `false` |

---

## 配置文件

1. [主配置](docs/configs/main.md)
2. [API_INFO](docs/configs/api_info.md)
3. [Blacklist](docs/configs/blacklist.md)
4. [User_Nickname_Mapping](docs/configs/uer_nickname_mapping.md)

---

## Markdown图片渲染

请参阅：
[Markdown图片渲染模板](docs/markdown_render/template.md)
[Markdown图片渲染样式](docs/markdown_render/style.md)

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
详情请参阅：[模板展开系统](docs/template_expansion_engine/main.md)

---

## 接口表

请参阅：[接口表](docs/api_table.md)

---

## 多模态输入

在 `/chat/completion` 端点下面
传入 `image_url` 即可让后端构造视觉模态请求
但需要保证目标模型支持视觉模态输入

其他模态输入暂不支持

---

## 用户配置

请参阅：[用户配置](docs/configs/user_config.md)

---

## 相关仓库

[Sloves_Starter](https://github.com/qeggs-dev/Sloves_Starter)