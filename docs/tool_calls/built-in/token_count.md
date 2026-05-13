# Token Count

让 AI 知道你有记录以来，消耗了多少 Token

注册名：`token_count`

返回结果
``` json
{
  "total_tokens": 246, // The total token count.
  "input_tokens": 123, // The token count of the input. 
  "output_tokens": 123, // The token count of the output.
  "cache_hit_count": 123, // The number of cache hits.
  "cache_miss_count": 0 // The number of cache misses.
}
```