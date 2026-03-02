# Nexus API

Nexus 是 Repeater 的共享 JSON 存储服务
用于在多个用户甚至多个实例之间传递数据

Repeater 提供了如下对接 Nexus 的接口：
- [Upload API](./upload.md)
- [Download API](./download.md)

预期的 Nexus Pool 白名单：
- `repeater.context`
- `repeater.prompt`
- `repeater.config`
- `repeater.environment`

预期的 Nexus 版本：`1.0.0.0`