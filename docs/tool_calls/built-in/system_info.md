# System Info

获取系统信息

注册名：`system_info`

返回当前的系统信息：
``` json
{
  "name": "Repeater AI System", // Repeater AI System Name
  "version": "x.x.x.x", // Repeater AI System Version
  "author": "Qeggs", // Repeater AI System Author
  "license": "MIT", // Repeater AI System License
  "copyright": "Copyright (c) 2025 Qeggs", // Repeater AI System Copyright
  "github": [...], // Repeater AI System Github Repositories
  "system_identificationConfig": {
    "system_name": "Repeater AI System", // Repeater AI System Name
    "system_ua": "Repeater AI System", // Repeater AI System User-Agent
    "crawler_name": "Repeater AI Crawler", // Repeater AI System Crawler Name
  },
  "runtime": "Python 3.11.x (tags/v3.11.x:xxxxxx, xxx  x xxxx, xx:xx:xx) [Platform] on xxx", // Repeater AI System Runtime
}
```

返回内容可被配置修改