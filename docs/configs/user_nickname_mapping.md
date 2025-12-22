# User Nickname Mapping 配置文件

这个配置文件
用于根据用户的 `user_name` 或 `user_id` 映射一个用户名
通常在用户自己传入的用户名会导致问题时
使用这个配置文件来映射一个用户名
以避免模型错误或陷入循环

文件格式如下：
```json
{
    "user_name": "user_name_nickname",
    "user_id": "user_id_nickname"
}
```
这样写的话
如果 `user_name` 是 `user_name`，那么它的昵称就是 `user_name_nickname`。
如果 `user_id` 是 `user_id`，那么它的昵称就是 `user_id_nickname`。