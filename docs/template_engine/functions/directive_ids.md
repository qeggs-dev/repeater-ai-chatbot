# Directive Ids Function

- `directive_ids`
  - Params:
    - `base_type` (list[str]): 基础类型，通常用于指定根目录
  - Returns:
    - (AsyncGenerator[tuple[str, str], None]):
      - 返回所有指定类型的 Directive 类型与 ID