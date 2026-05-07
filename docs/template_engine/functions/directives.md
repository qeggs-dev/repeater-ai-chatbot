# Directives Function

- `directives`
  - Params:
    - `base_type` (list[str]): 基础类型，通常用于指定根目录
  - Returns:
    - (AsyncGenerator[str, None, None]):
      - 返回所有已渲染的 Prompt Directives