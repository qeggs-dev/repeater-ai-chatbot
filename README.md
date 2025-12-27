# @复读机Repeater
**- Only Chat, Focus Chat. -**

一个主要基于[`OpenAI SDK`](https://pypi.org/project/openai/)开发的聊天机器人
将原始会话数据的处理直接公开给用户使用
以达到接近直接操作API的灵活度体验

目前，复读机具有以下特点：

 - 平行数据管理：支持平行数据管理，用户可以随意切换平行数据，减少数据丢失的风险
 - 多模型支持：支持OpenAI接口的对话模型即可调用，可以根据需要选择不同的模型进行对话
 - 更高自由度：用户可以自定义会话注入、切换、删除，以及自定义提示词和模型参数
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

## 详细文档

[详细文档](./docs/index.md)
从这里开始使用 Repeater!

---

## 功能拓展

Repeater 的功能拓展主要靠编写对应领域的 Client
比如，你可以使用 Repeater 的 API 来制作一个每天自动写日记的 Client
或者，将其接入到其他地方，以减少手动维护状态的成本

---

## 项目设计

> 这个项目在最初只是为了给 Bot 添加方便的有状态 AI API
> 后面逐渐发现，这个项目其实可以独立出去，作为一个单独的项目使用
> 设计理念上，Repeater 希望用户能完全掌握自己的数据 (别把锅甩运营头上)
> Repeater 并不主动的把目标放在拟人化上，工具的行为越清晰，用户越能对工具放心
> 它希望在有人与它进行交流时，能时刻想起自己可以对自己才是有控制权的那方
> (我才不会告诉你是因为我不会写拟人化才走的这条路呢)

---

## 相关仓库

[Sloves_Starter](https://github.com/qeggs-dev/Sloves_Starter)