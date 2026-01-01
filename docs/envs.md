# 环境变量表

用于引导主配置
添加 API_Key
以及设置一些服务器启动配置

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