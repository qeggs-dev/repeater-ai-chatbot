# 配置文件

用于对 Repeater 进行全局配置
Repeater 会首先从 `CONFIG_DIR` 环境变量
指定的目录去遍历`.md`文件，并加载配置文件。
加载后的配置文件按照路径名称进行排序后
进行合并处理
排名在后的会覆盖在前面的配置项。

PS: 配置读取时键名不区分大小写，但建议使用小写格式
配置管理器会递归扫描环境变量`CONFIG_DIR`下的所有json/yaml文件
并按照路径的字符串顺序排列，后加载配置中的字段会覆盖之前的配置
你也可以使用环境变量`CONFIG_FORCE_LOAD_LIST`来强制按照指定的顺序加载配置


## 最小配置

配置文件的所有字段都有默认值，你只需要填写你需要的部分即可
比如：
``` json
{
    "api_info": {
        // 必须要定义模型，否则Repeater可能会不知道你要给谁发请求
        "api_file_path": "./config/api_info.json",
        // 这里非常建议你填写，因为默认的`chat`真的很容易冲突
        "default_model_uid": "deepseek-chat"
    },
    "logger": {
        // 建议填写，默认的是DEBUG，它的输出有点多
        "level": "INFO"
    },
    "render": {
        "to_image": {
            // 也建议填写，除非你对 playwright 安装了独立的浏览器
            "executable_path" : "" // 这里填写你安装的任意浏览器可执行文件的路径
        }
    }
}
```

当你不知道如何配置时，直接运行程序
它可以给你自动生成一份默认配置文件

## 详细字段信息：
```json
{
    // API INFO 配置
    "api_info": {
        // API INFO 文件路径
        "api_file_path": "./config/api_info.json",

        // 默认使用的模型uid
        // 这里需要填写你在api_info.json中配置的模型uid
        // 如果用户没有指定模型，则使用这个模型进行响应
        // uid匹配默认是不分大小写的
        // 不建议使用默认UID，因为chat指定的太过宽泛
        // 建议在部署时，自己定一个或是根据厂商和模型的名字来定一个
        // 比如deepseek-chat之类的
        "default_model_uid": "chat",

        // 在匹配UID时是否启用大小写敏感
        // 此选项需要更改后需要重新录入API INFO
        // 因为 API INFO 中实现这个的方法是全部转换为小写
        "case_sensitive": false
    },
    "blacklist": {
        // 黑名单配置

        // 黑名单文件路径
        // 嗯这个文件只需要在开头写一个`[REGEX PARALLEL FILE]`
        // 然后下面每一行一个正则表达式就行了
        // 如果没有你也可以不写
        // 但是文件头必须有
        "file_path": "./config/blacklist.regex",

        // 黑名单匹配超时时间，单位为秒
        "match_timeout": 10.0 // 匹配超时时间，单位为秒
    },

    // CallAPI 配置
    "callapi": {
        // 协程池最大并发数
        // 仅在 AI 请求路径下生效
        "max_concurrency": 1000,

        // 当为 true 时，将启用流混淆。
        // 流混淆会在流 delta 事件的 `obfuscation` 字段中添加随机字符，
        // 提高攻击者根据长度去推断模型输出内容的难度
        "include_obfuscation":false,

        // 用于在某些API下告诉服务方
        // 自己是否需要返回Usage信息
        // 默认值：true，因为 Fast Statistics 需要这部分数据
        "include_usage": true
    },

    // Context 配置
    "context": {
        // 自动上下文长度裁剪
        // 当你聊天过长时，可能会超过模型上下文窗口限制
        // 这个设置可以让Repeater为你自动裁剪最久的消息
        // 让你可以继续聊天
        // 默认值：null，表示不启用
        // 你可以在这里填写一个整数，表示自动裁剪的长度，单位为字符数量
        "context_shrink_limit": null,
        
        // 是否在用户未指定的情况下
        // 保存用户的上下文历史
        "save_context": true,

        // 是否丢弃非文本数据
        // 只保存文本，不保存图片，音频等其他数据
        // 默认为false
        // 设为true可能会让你获得更快的解析速度
        "save_text_only": false,

        // 非文本数据在日志中的最大显示长度
        // 默认为 null，表示不限制
        "max_log_length_for_non_text_content": 25
    },

    // 全局异常处理器配置
    "global_exception_handler": {
        // 当异常未被处理时，服务器返回的错误信息
        "error_message": "Internal Server Error",

        // 遇到关键错误是，服务器返回的错误信息
        "critical_error_message": "Critical Server Error!",

        // 在遇到关键错误时，是否让服务器关闭
        "crash_exit": true,

        // 遇到问题时，保存 traceback 的目录
        // 如果该值为 null 则程序会跳过这一步骤
        // 但日志中的错误追踪不受影响
        "traceback_save_to": "./workspace/crash_log",

        // 是否记录所有异常(比如 KeyboardInterrupt)
        "record_all_exceptions": true,

        // 代码读取器配置
        // 通常是为了更直观的显示错误位置
        "code_reader": {
            // 是否启用代码读取器
            "enable": true,

            // 读取代码文件时使用的编码
            "code_encoding": "utf-8",

            // 读取代码文件从错误发生行开始向两边扩展的行数
            "code_line_dilation": 3,

            // 读取时是否添加行数标记
            "with_numbers": true,

            // 行数标记所占用的字符长度
            // 默认为5
            // 即行数在5个字符的最右边
            // 举例：
            // |    1| def foo():
            // |>   2|     raise Exception("Error")
            "reserve_space": 5,

            // 行数标记填充字符
            // 通常为空格
            "fill_char": " ",

            // 添加底部边框
            // 一般长度上限为终端宽度减去行数标记所占的长度
            "add_bottom_border": true,

            // 底部边框延长线的长度上限
            // 当值为 null 时，将使用终端宽度减去行数标记所占的长度
            "bottom_border_limit": null
        },

        // 使用 Repeater 自己的 Traceback 格式化函数
        "repeater_traceback": {
            // 是否启用
            "enable": false,

            // 是否排除库函数的 Traceback
            "exclude_library_code": true,
        
            // 是否使用自定义的 pydantic.ValidationError 格式化信息
            "format_validation_error": true,

            // 是否记录警告信息
            "record_warnings": true,

            // 是否使用传统堆栈帧格式 (Python 原版 Traceback)
            "traditional_stack_frame": false,
        }
    },

    // Logger 配置
    "logger": {
        // Log 文件输出路径
        "file_path": "./logs/repeater-log-{time:YYYY-MM-DD_HH-mm-ss.SSS}.log",

        // Log 控制台输出格式
        "console_format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{extra[user_id]}</cyan> - <level>{message}</level>",

        // Log 文件输出格式
        "file_format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[user_id]} - {message}",

        // Log 级别
        "level": "INFO",

        // Log 轮换设置
        "rotation": "1 days",

        // Log 保留设置
        "retention": "1 months",

        // Log 过期后执行的操作
        "compression": "zip"
    },

    // 你可以微调默认的用户model参数
    // 如果用户没有定义模型参数，则你这里定义的参数取请求API
    "model": {
        // 默认模型超时时间，单位为秒
        "default_timeout": 600.0,

        // 默认模型温度，更高的温度意味着下一个词更高的不确定性
        "default_temperature": 1.0,

        // 默认模型Top_P，指越大在采样时考虑的词汇越多
        "default_top_p": 1.0,

        // 默认模型最大生成长度(兼容)
        "default_max_tokens": 4096,

        // 默认模型最大生成长度
        "default_max_completion_tokens": 4096,

        // 默认模型频率惩罚，值越高模型越不容易出现重复内容
        // 惩罚程度按照频率增加，如果该值为负则是奖励模型输出重复内容
        "default_frequency_penalty": 0.0,

        // 默认模型存在惩罚，值越高模型越不容易出现重复内容
        // 惩罚程度只要存在就一直不变，如果该值为负则是奖励模型输出重复内容
        "default_presence_penalty": 0.0,

        // 默认模型停止符
        // 当模型输出到停止符内容时，停止生成
        "default_stop": [],

        // 默认模型是否流式输出
        // 注意：这里只是在告诉Repeater应该使用什么方式调用模型接口
        // 如果模型不支持流式生成，调用可能会报错
        // 且该参数不能决定/chat/completion接口是否流式输出
        // 如果这里为false
        // 那么/chat/completion接口调用时stream参数能且只能为false
        // 此时如果客户端请求流式响应，会返回503错误
        // 请求控制台和日志不会显示生成过程，也不会有chunk统计数据
        // 如果这里为true
        // 那么/chat/completion接口调用时stream参数可以为true或false
        // 且控制台和日志会打印当前chunk，并生成chunk统计数据
        "stream": true
    },

    // template 提示词文本模板展开器配置
    // 注：此选项不会改变实际的其他系统内容，而只会改变模板展开器中的变量
    "prompt_template": {
        // 模板展开器中显示的程序版本
        // 如果为 null 或空字符串
        // 则程序会使用 core 版本号填充
        "version": null,

        // 模板展开器中显示的 Bot 信息
        "bot_info": {
            // 模板展开器中显示的 Bot 名称
            "name": "Repeater",
            // Bot 的生日
            "birthday": {
                "day": 28,
                "month": 6,
                "year": 2024
            }
        },
        "time": {
            // 时区字符串
            "timezone": "Asia/Shanghai"
        }
    },

    // Prompt 配置
    "prompt": {
        // 告诉Prompt加载器预设提示词目录的路径
        "dir": "./config/prompt/presets",

        // 预设提示词文件的后缀名
        "suffix": ".md",

        // 预设提示词文件应该用什么编码打开
        "encoding": "utf-8",

        // 如果用户没有指定用一个预设提示词时
        // 应该使用哪一个提示词
        "preset_name": "default",

        // 是否在用户未指定的情况下
        // 加载提示词
        "load_prompt": true
    },
    
    // Markdown 图片渲染器配置
    "render": {
        // 图片等待多少时间后被删除（URL有效时间）
        "default_image_timeout": 60.0,

        // Markdown 到 HTML 渲染配置
        "markdown": {
            // 默认样式
            "default_style": "light",

            // 样式文件目录
            "styles_dir": "./configs/styles",

            // 样式文件应该用什么编码打开
            "style_file_encoding": "utf-8",

            // HTML 模板文件目录
            "html_template_dir": "./configs/html_templates",

            // HTML 模板文件应该用什么编码打开
            "html_template_file_encoding": "utf-8",

            // 默认使用的 HTML 模板文件
            "default_html_template": "default.html",

            // Markdown 预处理器配置
            "preprocess_map": {
                // Before 预处理器
                // 处理 Markdown 数据
                "before": {},
                // After 预处理器
                // 处理 HTML 数据
                "after": {}
            },
            // 在 HTML 中添加的标题
            "title": "Repeater Image Generator"
        },

        // HTML 到图片的渲染器配置
        "to_image": {
            // 最多允许在一个浏览器中打开多少个页面
            "max_pages_per_browser": 5,

            // 最多允许同时打开的浏览器数量
            "max_browsers": 2,

            // 浏览器类型
            "browser_type": "msedge",

            // 浏览器是否为无头模式
            "headless": true,

            // 输出图片的目录
            "output_dir": "./workspace/temp/render",

            // 输出图片的格式
            "output_suffix": ".png",

            // 浏览器的可执行文件路径
            "executable_path": "",

            // 浏览器窗口大小
            "width": 1200,
            "height": 600
        }
    },

    // /chat/completion 端口的请求日志
    "request_log": {
        // 请求日志的保存目录
        "dir": "./workspace/request_log",

        // 是否自动保存请求日志
        "auto_save": true,

        // 缓存请求日志的等待时间
        "debonce_save_wait_time": 1200.0,

        // 请求日志缓存的队列最大长度
        "max_cache_size": 1000
    },

    // 服务器配置
    // 这里的几个字段为null或不填则会使用环境变量中定义的配置
    // 如果这里填写了内容，那么这里的内容会覆盖环境变量中的值
    "server": {
        // 监听的IP
        "host": null,

        // 监听的端口
        "port": null,

        // 工作进程数量
        "workers": null,

        // 是否在文件发生变动时自动重启
        "reload": null,

        // 是否启动服务器
        // 如果为 false
        // 那么在初始化结束后
        // 程序将会直接退出
        // 而不是启动服务器
        "run_server": true
    },
    // 静态文件配置
    "static": {
        // README.md 文件的路径
        "readme_file_path": "./README.md",

        // 静态文件目录
        "static_dir": "./static"
    },
    // 用户配置缓存配置
    "user_config_cache": {
        // 读取配置后等待多少秒后从缓存删除
        "downgrade_wait_time": 600.0,

        // 保存配置到缓存后等待多少秒后从关闭缓存并写入
        "debounce_save_wait_time": 1000.0
    },

    // 用户数据配置
    "user_data": {
        // 用户数据的保存目录
        "dir": "./workspace/data/user_data",

        // 分支数据使用的目录名称
        "branches_dir_name": "branches",

        // 元数据文件名称
        "metadata_file_name": "metadata.json",

        // 默认分支名称
        "default_branch_id": "main",

        // 是否在获取文件大小时 readable 里使用缩写
        "file_size_use_abbreviation": true,

        // 是否允许跨用户数据流
        // 如果为 true，则请求时按照请求的ID来加载数据
        // 否则，则按照当前的user_id来加载数据
        "allow_cross_user_data_flow": false,

        // 是否缓存
        // 这里的两个字段同时支持bool和cache_data结构
        // 如果为bool，则该值对所有数据类型生效
        // 如果为cache_data结构，则该值对指定的数据类型生效
        // 警告：缓存系统仍未进行可行性与稳定性验证，请谨慎使用

        // 是否缓存元数据
        "cache_medadata": false,
        // 是否缓存用户数据
        "cache_data": {
            "context": false,
            "prompt": false,
            "config": false
        }
    },

    // 用户昵称映射配置
    "user_nickname_mapping": {
        // 昵称映射文件路径
        // 有些用户的昵称可能会让模型陷入循环
        // 可以用这个文件来映射它们到一个安全的昵称
        "file_path": "./config/user_nickname_mapping.json"
    },

    // Web配置
    "web": {
        // Index Web 文件路径
        // 如果不填写这个项目，那么默认会使用内置的索引页面
        // 你也可以使用这个来为 Repeater 创建一个自定义前端
        "index_web_file": "./static/index.html"
    }
}
```