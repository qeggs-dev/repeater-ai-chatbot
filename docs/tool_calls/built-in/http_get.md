# HTTP GET Tool

该工具用于发送 HTTP GET 请求

``` json
{
    "url": "", // The URL to send the GET request to
    "params": null, // The parameters to include in the GET request
    "headers": null, // The headers to include in the GET request
    "cookies": null, // The cookies to include in the GET request
    "auth": null, // The authentication credentials to include in the GET request
    "follow_redirects": true, // Whether to follow redirects
    "timeout": 10 // The timeout for the GET request
}
```

然后拿到一个响应对象

```json
{
  "status_code": 200, // 状态码
  "reason": "success", // 只要响应了就是 `success` 而超时等情况会是其他内容
  "headers": {}, // 响应头
  "cookies": {}, // 响应 cookie
  "data": {} // 响应内容(如果 JSON 解析失败，则将响应文本作为 `data` 返回，解析成功则该字段为任意 JSON 对象)
}
```